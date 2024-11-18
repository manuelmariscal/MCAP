# sqlite_db.py

import sqlite3
from utils import Utils
from textblob import TextBlob
from colorama import Fore, Style
import os
import traceback

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
            traceback.print_exc()
            raise

    def create_tables(self):
        try:
            cursor = self.connection.cursor()
            # Habilitar soporte para claves foráneas
            cursor.execute("PRAGMA foreign_keys = ON;")
            # Creación de tablas con constraints de unicidad
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
            self.connection.commit()
            print(Fore.GREEN + "Tablas creadas exitosamente en SQLite." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Error al crear tablas en SQLite: {e}" + Style.RESET_ALL)
            traceback.print_exc()
            self.connection.rollback()
            raise

    def insert_data(self, tweets_data):
        try:
            if not tweets_data:
                print(Fore.YELLOW + "No hay datos de tweets para insertar en SQLite." + Style.RESET_ALL)
                return
            cursor = self.connection.cursor()

            for data in tweets_data:
                tweet = data['tweet']
                user = data['user']

                if not user:
                    print(Fore.YELLOW + "No se encontró información del usuario para un tweet. Saltando..." + Style.RESET_ALL)
                    continue  # Saltar si no hay información de usuario

                # Usuario
                cursor.execute("""
                    INSERT OR IGNORE INTO usuarios (usuario_id, nombre_usuario, seguidores, ubicacion, verificado)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    str(user.id),
                    user.username,
                    user.public_metrics.get('followers_count', 0),
                    user.location if hasattr(user, 'location') else None,
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
                    tweet.public_metrics.get('retweet_count', 0),
                    tweet.public_metrics.get('like_count', 0),
                    sentiment
                ))

            self.connection.commit()
            print(Fore.GREEN + "Datos insertados en SQLite exitosamente." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Error al insertar datos en SQLite: {e}" + Style.RESET_ALL)
            traceback.print_exc()
            self.connection.rollback()
            raise

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print(Fore.GREEN + "Conexión a SQLite cerrada." + Style.RESET_ALL)
