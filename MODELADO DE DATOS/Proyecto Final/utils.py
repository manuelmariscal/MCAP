# utils.py

from colorama import Fore, Style, init

class Utils:
    def __init__(self):
        init(autoreset=True)

    def get_keywords(self):
        try:
            keywords = input(Fore.BLUE + "Ingrese las palabras clave separadas por comas: " + Style.RESET_ALL)
            keywords_list = [kw.strip() for kw in keywords.split(',') if kw.strip()]
            if not keywords_list:
                print(Fore.RED + "Debe ingresar al menos una palabra clave." + Style.RESET_ALL)
                exit()
            return keywords_list
        except Exception as e:
            print(Fore.RED + f"Error al obtener palabras clave: {e}" + Style.RESET_ALL)
            exit()
