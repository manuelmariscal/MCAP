# openai_analysis.py

import openai
from utils import Utils
from colorama import Fore, Style
import os
from dotenv import load_dotenv

class OpenAIAnalysis:
    def __init__(self):
        self.utils = Utils()
        self.api_key = self.load_api_key()

    def load_api_key(self):
        try:
            load_dotenv()
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                print(Fore.RED + "Error: La clave de API de OpenAI no está configurada." + Style.RESET_ALL)
                raise Exception("Clave de API de OpenAI no configurada")
            openai.api_key = api_key
            print(Fore.GREEN + "API de OpenAI configurada exitosamente." + Style.RESET_ALL)
            return api_key
        except Exception as e:
            print(Fore.RED + f"Error al configurar la API de OpenAI: {e}" + Style.RESET_ALL)
            raise

    def singularity(self, tweets_data, keywords):
        try:
            print(Fore.BLUE + "Realizando análisis con OpenAI..." + Style.RESET_ALL)
            # Preparar el contenido para enviar a OpenAI
            tweets_text = [data['tweet'].text for data in tweets_data]
            combined_text = "\n\n".join(tweets_text)

            # Crear el prompt para OpenAI
            prompt = f"""Analiza los siguientes tweets relacionados con {', '.join(keywords)} y proporciona un resumen de las tendencias, sentimientos y temas principales:

            {combined_text}

            Resumen:
            """

            # Llamar a la API de OpenAI
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=250,
                temperature=0.7,
                top_p=1,
                n=1,
                stop=None,
            )

            summary = response.choices[0].text.strip()
            print(Fore.CYAN + "Análisis de OpenAI completado:" + Style.RESET_ALL)
            print(summary)

            return summary
        except Exception as e:
            print(Fore.RED + f"Error en el análisis con OpenAI: {e}" + Style.RESET_ALL)
            return None
