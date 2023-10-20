# Imports 
import pandas as pd
import math
import googlemaps
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time
import datetime
import pyroutelib3
from pyroutelib3 import Router
import requests, json
import urllib.parse

KEY = 'AIzaSyBzwNjr0jEe67mqgMdU9w6RqU_AHGln8UM'

# Coordonnées des villes en France 
URL = "https://www.data.gouv.fr/fr/datasets/r/51606633-fb13-4820-b795-9a2a575a72f1"
df = pd.read_csv(URL)

# Liste des colonnes de df : ['insee_code', 'city_code', 'zip_code', 'label', 'latitude', 'longitude', 
#                            'department_name', 'department_number', 'region_name', 'region_geojson_name']


class CarNetwork():
    """
    Classe qui calcul le trajet optimal pour relier un point A à un point B avec une voiture électrique en France.

    Parameters:
    -----------
    A : adresse de départ  / format : numéro, rue, code postal ville (en minuscule)
    B : adresse d'arrivée / format : numéro, rue, code postal ville (en minuscule)
    Autonomie : Autonomie du véhicule utilisé

    Attributes:
    -----------
    x_A : (latitude, longitude) du point A
    x_B : (latitude, longitude) du point B

    Methods:
    --------
    get_coordo : permet de récupérer x_A et x_B
    calcul_distance_haversine : permet de calculer une distance à vol d'oiseau
    """

    def __init__(self, A, B, autonomie):
        self.A = A
        self.B = B
        self.autonomie = autonomie
        self.x_A = None
        self.x_B = None

    def get_coordo(self):
        """
        Permet de renvoyer (latitude,longitude)
        """
        dep_json_A = requests.get("https://api-adresse.data.gouv.fr/search/?q=" + urllib.parse.quote(self.A) + "&format=json").json()
        dep_json_B = requests.get("https://api-adresse.data.gouv.fr/search/?q=" + urllib.parse.quote(self.B) + "&format=json").json()
        self.x_A = list(dep_json_A['features'][0].get('geometry').get('coordinates'))
        self.x_B = list(dep_json_B['features'][0].get('geometry').get('coordinates'))

    def calcul_distance_haversine(self):
        """
        on utilise la distance de haversine
        -----------
        x_A = (latitude, longitude)
        x_B = (latitude, longitude)

        Peu efficace car distance à vol d'oiseau
        """
        reseau.get_coordo()

        # Rayon de la Terre en kilomètres
        R = 6371.0
        latitudeA, longitudeA = self.x_A
        latitudeA, longitudeA = math.radians(latitudeA), math.radians(longitudeA)
        latitudeB, longitudeB = self.x_B
        latitudeB, longitudeB = math.radians(latitudeB), math.radians(longitudeB)
        dlat = latitudeB - latitudeA
        dlon = longitudeB - longitudeA
        a = math.sin(dlat / 2)**2 + math.cos(latitudeA) * math.cos(latitudeB) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        # Distance en kilomètres
        distance = R * c
        return distance  


"""
def nearest_station(self):
    stations = data[['x_longitude', 'y_latitude']]
    coord_actuelle = np.array([self.position_actuelle[0], self.position_actuelle[1]])
    distances = distance.cdist(coord_actuelle, stations, metric='euclidean')
    indice_min_distance = np.argmin(distances)
    nearest_station = stations.iloc[indice_min_distance][['x_longitude', 'y_latitude']]

    return nearest_station  
"""

# Pour faire des tests
reseau = CarNetwork('1, rue Joliot Curie, 91190 Gif-sur-Yvette', '3, rue Dareau, 75014 Paris', 12)
reseau.get_coordo()
print(reseau.x_A, reseau.x_B)


