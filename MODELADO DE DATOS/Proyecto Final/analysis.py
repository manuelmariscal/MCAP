# analysis.py

from colorama import Fore, Style
import sqlite3

class Analyzer:
    def __init__(self, sqlite_db, neo4j_db):
        self.sqlite_db = sqlite_db
        self.neo4j_db = neo4j_db

    def run_analysis(self, keywords):
        print(Fore.BLUE + "Iniciando análisis de datos..." + Style.RESET_ALL)
        self.sentiment_analysis(keywords)
        self.top_influential_users(keywords)
        self.trend_over_time(keywords)

    def sentiment_analysis(self, keywords):
        try:
            cursor = self.sqlite_db.connection.cursor()
            format_strings = ','.join('?' * len(keywords))
            query = f"""
            SELECT sentimiento FROM tweets t
            JOIN tweets_palabrasclave tp ON t.tweet_id = tp.tweet_id
            JOIN palabras_clave pk ON tp.palabra_clave_id = pk.palabra_clave_id
            WHERE pk.texto IN ({format_strings})
            """
            cursor.execute(query, keywords)
            sentiments = [row[0] for row in cursor.fetchall()]
            if len(sentiments) > 0:
                avg_sentiment = sum(sentiments) / len(sentiments)
                print(Fore.CYAN + f"Sentimiento promedio: {avg_sentiment:.2f}" + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + "No hay suficientes datos para calcular el sentimiento promedio." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Error en análisis de sentimiento: {e}" + Style.RESET_ALL)

    def top_influential_users(self, keywords):
        try:
            cursor = self.sqlite_db.connection.cursor()
            format_strings = ','.join('?' * len(keywords))
            query = f"""
            SELECT u.nombre_usuario, SUM(t.retweets + t.likes) as influence FROM usuarios u
            JOIN tweets t ON u.usuario_id = t.usuario_id
            JOIN tweets_palabrasclave tp ON t.tweet_id = tp.tweet_id
            JOIN palabras_clave pk ON tp.palabra_clave_id = pk.palabra_clave_id
            WHERE pk.texto IN ({format_strings})
            GROUP BY u.usuario_id
            ORDER BY influence DESC
            LIMIT 5
            """
            cursor.execute(query, keywords)
            results = cursor.fetchall()
            if results:
                print(Fore.CYAN + "Usuarios más influyentes:" + Style.RESET_ALL)
                for row in results:
                    print(f"- {row[0]} con influencia {row[1]}")
            else:
                print(Fore.YELLOW + "No se encontraron usuarios influyentes." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Error en análisis de usuarios influyentes: {e}" + Style.RESET_ALL)

    def trend_over_time(self, keywords):
        try:
            cursor = self.sqlite_db.connection.cursor()
            format_strings = ','.join('?' * len(keywords))
            query = f"""
            SELECT substr(t.fecha_hora, 1, 10) as date, COUNT(*) as count FROM tweets t
            JOIN tweets_palabrasclave tp ON t.tweet_id = tp.tweet_id
            JOIN palabras_clave pk ON tp.palabra_clave_id = pk.palabra_clave_id
            WHERE pk.texto IN ({format_strings})
            GROUP BY date
            ORDER BY date
            """
            cursor.execute(query, keywords)
            results = cursor.fetchall()
            if results:
                print(Fore.CYAN + "Tendencia de tweets en el tiempo:" + Style.RESET_ALL)
                for row in results:
                    print(f"- {row[0]}: {row[1]} tweets")
            else:
                print(Fore.YELLOW + "No hay datos suficientes para mostrar tendencia en el tiempo." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Error en análisis temporal: {e
