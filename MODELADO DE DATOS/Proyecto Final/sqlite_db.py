# sqlite_db.py

import sqlite3
from utils import Utils
from textblob import TextBlob
from colorama import Fore, Style
import os

class SQLiteDatabase:
    def __init__(self):
        self.utils = Utils()
        self.connection = self.connect()

    def connect(self):
        try:
            # Crear directorio 'data' si no existe
            if not os.path.exists('data'):
                os.makedirs('data')
            # Conectar a la base de datos SQLite
            connection = sqlite3.connect('data/twitter.db')
            print(Fore.GREEN + "Conectado a la base de datos SQLite exitosamente." + Style.RESET_ALL)
            return connection
        except Exception as e:
            print(Fore.RED + f"Error al conectar a SQLite: {e}" + Style.RESET_ALL)
            raise

    def create_tables(self):
        try:
            cursor = self.connection.cursor()
            # Habilitar soporte para claves foráneas
            cursor.execute("PRAGMA foreign_keys = ON;")
            # Creación de tablas
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                usuario_id TEXT PRIMARY KEY,
                nombre_usuario TEXT,
                seguidores INTEGER,
                ubicacion TEXT,
                verificado BOOLEAN
            );
            """)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS tweets (
                tweet_id TEXT PRIMARY KEY,
                usuario_id TEXT,
                contenido TEXT,
                fecha_hora TEXT,
                retweets INTEGER,
                likes INTEGER,
                sentimiento REAL,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id)
            );
            """)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS palabras_clave (
                palabra_clave_id INTEGER PRIMARY KEY AUTOINCREMENT,
                texto TEXT
            );
            """)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS tweets_palabrasclave (
                tweet_id TEXT,
                palabra_clave_id INTEGER,
                PRIMARY KEY (tweet_id, palabra_clave_id),
                FOREIGN KEY (tweet_id) REFERENCES tweets(tweet_id),
                FOREIGN KEY (palabra_clave_id) REFERENCES palabras_clave(palabra_clave_id)
            );
            """)
            self.connection.commit()
            print(Fore.GREEN + "Tablas creadas exitosamente en SQLite." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Error al crear tablas en SQLite: {e}" + Style.RESET_ALL)
            self.connection.rollback()
            raise

    def insert_data(self, tweets_data, keywords):
        try:
            cursor = self.connection.cursor()
            # Insertar palabras clave
            keyword_ids = {}
            for kw in keywords:
                cursor.execute("INSERT INTO palabras_clave (texto) VALUES (?)", (kw,))
                keyword_ids[kw] = cursor.lastrowid

            for data in tweets_data:
                tweet = data['tweet']
                user = data['user']

                if not user:
                    continue  # Saltar si no hay información de usuario

                # Usuario
                cursor.execute("""
                    INSERT OR IGNORE INTO usuarios (usuario_id, nombre_usuario, seguidores, ubicacion, verificado)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    str(user.id),
                    user.username,
                    user.public_metrics['followers_count'],
                    user.location if 'location' in user else None,
                    user.verified
                ))

                # Sentimiento
                analysis = TextBlob(tweet.text)
                sentiment = analysis.sentiment.polarity

                # Tweet
                cursor.execute("""
                    INSERT OR IGNORE INTO tweets (tweet_id, usuario_id, contenido, fecha_hora, retweets, likes, sentimiento)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    str(tweet.id),
                    str(user.id),
                    tweet.text,
                    tweet.created_at.isoformat(),
                    tweet.public_metrics['retweet_count'],
                    tweet.public_metrics['like_count'],
                    sentiment
                ))

                # Asociar tweet con palabras clave
                for kw in keywords:
                    if kw.lower() in tweet.text.lower():
                        cursor.execute("""
                            INSERT OR IGNORE INTO tweets_palabrasclave (tweet_id, palabra_clave_id)
                            VALUES (?, ?)
                        """, (str(tweet.id), keyword_ids[kw]))

            self.connection.commit()
            print(Fore.GREEN + "Datos insertados en SQLite exitosamente." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Error al insertar datos en SQLite: {e}" + Style.RESET_ALL)
            self.connection.rollback()
            raise

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print(Fore.GREEN + "Conexión a SQLite cerrada." + Style.RESET_ALL)
