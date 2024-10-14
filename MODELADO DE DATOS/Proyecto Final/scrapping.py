import requests
from bs4 import BeautifulSoup
import sqlite3
from neo4j import GraphDatabase
from pyspark.sql import SparkSession
from datetime import datetime
import logging
import os

# Configuración de log
logging.basicConfig(level=logging.INFO)

class AmazonScraper:
    def __init__(self):
        self.base_url_bestsellers = 'https://www.amazon.com.mx/gp/bestsellers'
        self.base_url_deals = 'https://www.amazon.com.mx/deals?discounts-widget=%2522%257B%255C%2522state%255C%2522%253A%257B%255C%2522refinementFilters%255C%2522%253A%257D%257D%252C%255C%2522version%255C%2522%253A1%257D%2522'
        self.mysql_conn = self.connect_sqlite()  # Usamos SQLite
        self.neo4j_driver = self.connect_neo4j()
        self.spark = SparkSession.builder.appName("AmazonScraper").getOrCreate()

    def connect_sqlite(self):
        try:
            conn = sqlite3.connect('./amazon.db')  # Conexión a tu archivo de base de datos SQLite
            return conn
        except sqlite3.Error as err:
            logging.error(f"Error connecting to SQLite: {err}")
            return None

    def connect_neo4j(self):
        try:
            driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "your_password"))
            return driver
        except Exception as e:
            logging.error(f"Error connecting to Neo4j: {e}")
            return None

    def fetch_best_sellers(self):
        try:
            response = requests.get(self.base_url_bestsellers)
            soup = BeautifulSoup(response.text, 'html.parser')

            products = soup.find_all('a', {'class': 'a-link-normal aok-block'})  # Ajustar selector
            logging.info(f"Found {len(products)} products")  # Imprimir cuántos productos encontramos

            product_list = []

            for product in products:
                try:
                    # Extraer el nombre del producto
                    product_name = product.get_text(strip=True)
                    logging.info(f"Product Name: {product_name}")  # Verificar si se extrae el nombre

                    # Extraer el link del producto
                    product_link = 'https://www.amazon.com.mx' + product['href']

                    # Extraer el precio asociado
                    price_parent = product.find_next('span', {'class': 'a-price'})
                    if price_parent:
                        product_price = price_parent.find('span', {'class': 'a-price-whole'})
                        if product_price:
                            product_price = product_price.get_text(strip=True)
                            logging.info(f"Product Price: {product_price}")  # Verificar si se extrae el precio
                        else:
                            logging.warning("Price not found for this product")
                    else:
                        logging.warning("Price parent not found for this product")

                    product_list.append({
                        'name': product_name,
                        'price': float(product_price.replace('$', '').replace(',', '')) if product_price else None,
                        'link': product_link,
                        'category': 'Best Seller'
                    })

                except AttributeError as e:
                    logging.warning(f"Could not extract price or name for a product: {e}")
                    continue

            return product_list
        except Exception as e:
            logging.error(f"Error fetching best sellers: {e}")
            return []

    def fetch_deals(self):
        try:
            response = requests.get(self.base_url_deals)
            soup = BeautifulSoup(response.text, 'html.parser')
            deals = soup.find_all('a', {'class': 'dealTitle'})
            product_list = []
            for deal in deals:
                product_url = 'https://www.amazon.com.mx' + deal['href']
                product_detail = self.fetch_product_detail(product_url)
                if product_detail:
                    product_list.append(product_detail)
            return product_list
        except Exception as e:
            logging.error(f"Error fetching deals: {e}")
            return []

    def fetch_product_detail(self, url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            name = soup.find('span', {'id': 'productTitle'}).text.strip()
            price = soup.find('span', {'class': 'priceBlockBuyingPriceString'}).text.replace('$', '').replace(',', '')
            return {
                'name': name,
                'price': float(price),
                'category': 'Deals'
            }
        except Exception as e:
            logging.error(f"Error fetching product detail: {e}")
            return None

    def store_data_sqlite(self, product_list):
        cursor = self.mysql_conn.cursor()
        try:
            for product in product_list:
                cursor.execute("""
                    INSERT INTO products (name, price, category, created_at)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(name) DO UPDATE SET price=?, updated_at=?
                """, (product['name'], product['price'], product['category'], datetime.now(), product['price'], datetime.now()))
            self.mysql_conn.commit()
        except sqlite3.Error as err:
            logging.error(f"Error storing data in SQLite: {err}")

    def store_data_neo4j(self, product_list):
        session = self.neo4j_driver.session()
        try:
            for product in product_list:
                session.run("""
                    MERGE (p:Product {name: $name})
                    SET p.price = $price, p.category = $category
                    MERGE (c:Category {name: $category})
                    MERGE (p)-[:BELONGS_TO]->(c)
                """, name=product['name'], price=product['price'], category=product['category'])
        except Exception as e:
            logging.error(f"Error storing data in Neo4j: {e}")
        finally:
            session.close()

    def run(self):
        best_sellers = self.fetch_best_sellers()
        deals = self.fetch_deals()
        all_products = best_sellers + deals

        if all_products:
            self.store_data_sqlite(all_products)
            self.store_data_neo4j(all_products)

# Ejecución del scraper
if __name__ == "__main__":
    scraper = AmazonScraper()
    scraper.run()
