# twitter_api.py

import tweepy
from utils import Utils
from colorama import Fore, Style
import os
from dotenv import load_dotenv

class TwitterAPI:
    def __init__(self):
        self.utils = Utils()
        self.client, self.api_v1 = self.authenticate()

    def authenticate(self):
        try:
            # Cargar variables de entorno
            load_dotenv()
            bearer_token = os.getenv('TWITTER_BEARER_TOKEN')

            # Claves para autenticación OAuth 1.0a (necesarias para publicar tweets)
            consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
            consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
            access_token = os.getenv('TWITTER_ACCESS_TOKEN')
            access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

            if not all([bearer_token, consumer_key, consumer_secret, access_token, access_token_secret]):
                print(Fore.RED + "Error: Las credenciales de la API de Twitter no están completas." + Style.RESET_ALL)
                raise Exception("Credenciales de Twitter incompletas")

            # Cliente para lectura (API v2)
            client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)

            # Autenticación para publicar tweets (API v1.1)
            auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
            api_v1 = tweepy.API(auth)

            print(Fore.GREEN + "Autenticado con la API de Twitter exitosamente." + Style.RESET_ALL)
            return client, api_v1
        except Exception as e:
            print(Fore.RED + f"Error al autenticar con Twitter API: {e}" + Style.RESET_ALL)
            raise

    def search_tweets(self, keywords):
        try:
            query = ' OR '.join(keywords)
            print(Fore.BLUE + f"Buscando tweets para: {', '.join(keywords)}" + Style.RESET_ALL)
            # Realizar la búsqueda con un máximo de 7 tweets
            response = self.client.search_recent_tweets(
                query=query,
                max_results=7,
                tweet_fields=['created_at', 'text', 'public_metrics', 'lang', 'author_id'],
                expansions=['author_id'],
                user_fields=['username', 'name', 'public_metrics', 'verified', 'location']
            )
            tweets = response.data if response.data else []
            users = {u['id']: u for u in response.includes['users']} if response.includes and 'users' in response.includes else {}

            # Combinar la información de tweets y usuarios
            tweets_data = []
            for tweet in tweets:
                user = users.get(tweet.author_id)
                tweets_data.append({
                    'tweet': tweet,
                    'user': user
                })

            print(Fore.GREEN + f"Se obtuvieron {len(tweets)} tweets." + Style.RESET_ALL)
            return tweets_data
        except Exception as e:
            print(Fore.RED + f"Error al buscar tweets: {e}" + Style.RESET_ALL)
            return []

    def post_tweet(self, text):
        try:
            # Publicar el tweet
            self.api_v1.update_status(status=text)
            print(Fore.GREEN + "Tweet publicado exitosamente." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Error al publicar el tweet: {e}" + Style.RESET_ALL)

    def close_connection(self):
        # No es necesario cerrar conexiones explícitamente
        pass
