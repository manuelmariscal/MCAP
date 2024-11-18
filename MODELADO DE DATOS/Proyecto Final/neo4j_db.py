# neo4j_db.py

from neo4j import GraphDatabase
from utils import Utils
from textblob import TextBlob
from colorama import Fore, Style
import os
from dotenv import load_dotenv

class Neo4jDatabase:
    def __init__(self):
        self.utils = Utils()
        self.driver = self.connect()

    def connect(self):
        try:
            # Cargar variables de entorno
            load_dotenv()
            uri = "bolt://localhost:7687"
            user = "neo4j"
            password = os.getenv('NEO4J_PASSWORD')

            if not password:
                print(Fore.RED + "Error: La contraseña de Neo4j no está configurada." + Style.RESET_ALL)
                raise Exception("Contraseña de Neo4j no configurada")

            driver = GraphDatabase.driver(uri, auth=(user, password))
            print(Fore.GREEN + "Conectado a la base de datos Neo4j exitosamente." + Style.RESET_ALL)
            return driver
        except Exception as e:
            print(Fore.RED + f"Error al conectar a Neo4j: {e}" + Style.RESET_ALL)
            raise

    def create_constraints(self):
        try:
            with self.driver.session() as session:
                # Constraints para unicidad
                session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (u:Usuario) REQUIRE u.usuario_id IS UNIQUE")
                session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (t:Tweet) REQUIRE t.tweet_id IS UNIQUE")
                session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (p:PalabraClave) REQUIRE p.texto IS UNIQUE")
            print(Fore.GREEN + "Constraints creados en Neo4j." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Error al crear constraints en Neo4j: {e}" + Style.RESET_ALL)
            raise

    def insert_data(self, tweets_data, keywords):
        try:
            with self.driver.session() as session:
                # Insertar palabras clave
                for kw in keywords:
                    session.run("""
                        MERGE (p:PalabraClave {texto: $texto})
                    """, texto=kw)
                for data in tweets_data:
                    tweet = data['tweet']
                    user = data['user']

                    if not user:
                        continue  # Saltar si no hay información de usuario

                    # Usuario
                    session.run("""
                        MERGE (u:Usuario {usuario_id: $usuario_id})
                        SET u.nombre_usuario = $nombre_usuario,
                            u.seguidores = $seguidores,
                            u.ubicacion = $ubicacion,
                            u.verificado = $verificado
                    """, usuario_id=str(user.id),
                         nombre_usuario=user.username,
                         seguidores=user.public_metrics['followers_count'],
                         ubicacion=user.location if 'location' in user else None,
                         verificado=user.verified)
                    # Sentimiento
                    analysis = TextBlob(tweet.text)
                    sentiment = analysis.sentiment.polarity
                    # Tweet
                    session.run("""
                        MERGE (t:Tweet {tweet_id: $tweet_id})
                        SET t.contenido = $contenido,
                            t.fecha_hora = $fecha_hora,
                            t.retweets = $retweets,
                            t.likes = $likes,
                            t.sentimiento = $sentimiento
                    """, tweet_id=str(tweet.id),
                         contenido=tweet.text,
                         fecha_hora=tweet.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                         retweets=tweet.public_metrics['retweet_count'],
                         likes=tweet.public_metrics['like_count'],
                         sentimiento=sentiment)
                    # Relación PUBLICA
                    session.run("""
                        MATCH (u:Usuario {usuario_id: $usuario_id}), (t:Tweet {tweet_id: $tweet_id})
                        MERGE (u)-[:PUBLICA]->(t)
                    """, usuario_id=str(user.id), tweet_id=str(tweet.id))
                    # Relación ASOCIADO_A
                    for kw in keywords:
                        if kw.lower() in tweet.text.lower():
                            session.run("""
                                MATCH (t:Tweet {tweet_id: $tweet_id}), (p:PalabraClave {texto: $texto})
                                MERGE (t)-[:ASOCIADO_A]->(p)
                            """, tweet_id=str(tweet.id), texto=kw)
            print(Fore.GREEN + "Datos insertados en Neo4j exitosamente." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Error al insertar datos en Neo4j: {e}" + Style.RESET_ALL)
            raise

    def close_connection(self):
        self.driver.close()
        print(Fore.GREEN + "Conexión a Neo4j cerrada." + Style.RESET_ALL)
