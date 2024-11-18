# main.py

import sys
from twitter_api import TwitterAPI
from sqlite_db import SQLiteDatabase
from neo4j_db import Neo4jDatabase
from analysis import Analyzer
from openai_analysis import OpenAIAnalysis
from utils import Utils
from colorama import Fore, Style

def main():
    try:
        # Inicialización de utilidades
        utils = Utils()

        # Solicitar palabras clave al usuario
        keywords = utils.get_keywords()

        # Verificar que hay palabras clave
        if not keywords:
            print(Fore.YELLOW + "No se proporcionaron palabras clave. Terminando el programa." + Style.RESET_ALL)
            sys.exit()

        # Inicialización de la API de Twitter
        twitter_api = TwitterAPI()

        # Obtener tweets basados en las palabras clave
        tweets_data = twitter_api.search_tweets(keywords)

        if not tweets_data:
            print(Fore.YELLOW + "No se encontraron tweets para las palabras clave proporcionadas." + Style.RESET_ALL)
            sys.exit()

        # Conexión a la base de datos SQLite
        sqlite_db = SQLiteDatabase()
        sqlite_db.create_tables()
        sqlite_db.insert_data(tweets_data, keywords)

        # Conexión a la base de datos Neo4j
        neo4j_db = Neo4jDatabase()
        neo4j_db.create_constraints()
        neo4j_db.insert_data(tweets_data, keywords)

        # Análisis de datos
        analyzer = Analyzer(sqlite_db, neo4j_db)
        analyzer.run_analysis(keywords)

        # Análisis con OpenAI
        openai_analysis = OpenAIAnalysis()
        summary = openai_analysis.singularity(tweets_data, keywords)

        if summary:
            # Publicar el resumen en Twitter
            twitter_api.post_tweet(summary)
            print(Fore.GREEN + "El resumen se ha publicado en Twitter exitosamente." + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + "No se pudo generar el resumen con OpenAI." + Style.RESET_ALL)

        # Cerrar conexiones
        sqlite_db.close_connection()
        neo4j_db.close_connection()
        twitter_api.close_connection()

        print(Fore.GREEN + "Análisis completado exitosamente." + Style.RESET_ALL)

    except Exception as e:
        print(Fore.RED + f"Ocurrió un error: {e}" + Style.RESET_ALL)
        sys.exit(1)

if __name__ == "__main__":
    main()
