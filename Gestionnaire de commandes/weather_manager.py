# weather_manager.py
import requests
import io
import time
import pygame
from config_loader import CONFIG

# Parametres API
api_key = CONFIG["weather"]["api_key"]
location = CONFIG["weather"]["location"]
country_code = CONFIG["weather"]["country_code"]
language = CONFIG["weather"]["language"]
units = CONFIG["weather"]["units"]

# Variables globales pour la température et l'icone
temperature = None
icon_surface = None
last_fetched = None  # Pour grer le cache de la derniere requete

# Fonction pour récupérer la météo
def get_weather():
    global temperature, icon_surface, last_fetched

    # Si la température et l'icone ont été récupérées récemment, utiliser les valeurs en cache
    if last_fetched and time.time() - last_fetched < 600:  # 10 minutes en secondes
        return temperature, icon_surface
    
    url = f'http://api.openweathermap.org/data/2.5/weather?q={location},{country_code}&lang={language}&units={units}&appid={api_key}'
    
    try:
        response = requests.get(url)
        data = response.json()

        # Récupérer la température
        if 'main' in data:
            temperature = f"{int(round(data['main']['temp']))}°C"
        else:
            temperature = "Temperature non disponible"

        # Récupérer l'icone météo
        try:
            weather_icon = data['weather'][0]['icon']
            icon_url = f"http://openweathermap.org/img/wn/{weather_icon}@2x.png"
            icon_response = requests.get(icon_url)
            icon_image = pygame.image.load(io.BytesIO(icon_response.content))
            icon_surface = pygame.transform.smoothscale(icon_image, (50, 50))
        except Exception as e:
            print(f"Erreur de récupération de l'icone météo: {e}")
            icon_surface = None

        last_fetched = time.time()  # Mettre a jour le moment de la derniere récupération
        return temperature, icon_surface
    except Exception as e:
        print(f"Erreur de récupération des données météo: {e}")
        return "Température non disponible", None
