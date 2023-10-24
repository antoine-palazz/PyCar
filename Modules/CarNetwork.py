# Imports 
import pandas as pd
import math
# import googlemaps
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
import folium 

KEY = 'AIzaSyBzwNjr0jEe67mqgMdU9w6RqU_AHGln8UM'

# Coordonnées des villes en France 
URL = "https://www.data.gouv.fr/fr/datasets/r/51606633-fb13-4820-b795-9a2a575a72f1"

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
    url : lien qui encapsule la base de donnée sur laquelle repose la classe, ici la base de donnée considérée est 
    celle donnée par l'URL : 'https://www.data.gouv.fr/fr/datasets/r/517258d5-aee7-4fa4-ac02-bd83ede23d25'

    Attributes:
    -----------
    x_A : (latitude, longitude) du point A
    x_B : (latitude, longitude) du point B
    df : base de données sur laquelle repose la classe. On la défini à partir d'un URL

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
        self.stations_data = pd.read_csv('https://www.data.gouv.fr/fr/datasets/r/517258d5-aee7-4fa4-ac02-bd83ede23d25', sep = ',')

    def clean_data(self):
        '''
        Les coordonnées de longitude > 90 ou de latitude > 90 sont inutiles car elles dépassent les limites 
        des valeurs possibles pour la longitude (de -180 à 180) et la latitude (de -90 à 90) sur la surface 
        de la Terre, et donc, elles sont généralement considérées comme des données incorrectes. 
        La routine supprime ces données du dataframe.
        '''


        liste = []
    
        for row in self.stations_data.itertuples():

            if row.xlongitude > 90 or row.ylatitude > 90:
                liste.append(row.Index)

        self.stations_data.drop(liste)


    def get_coordo(self):
        """
        Permet de renvoyer (latitude,longitude)
        """
        dep_json_A = requests.get("https://api-adresse.data.gouv.fr/search/?q=" + urllib.parse.quote(self.A) + "&format=json").json()
        dep_json_B = requests.get("https://api-adresse.data.gouv.fr/search/?q=" + urllib.parse.quote(self.B) + "&format=json").json()
        self.x_A = list(dep_json_A['features'][0].get('geometry').get('coordinates'))
        self.x_B = list(dep_json_B['features'][0].get('geometry').get('coordinates'))


    def trajet_voiture(coor_depart, coor_arrivee, idf):
    
        router = pyroutelib3.Router("car")
        depart = router.findNode(coor_depart[0], coor_depart[1])
        #print(depart)
        arrivee = router.findNode(coor_arrivee[0], coor_arrivee[1])
        #print(arrivee)

        routeLatLons=[coor_depart,coor_arrivee]
        
        status, route = router.doRoute(depart, arrivee)
        if status == 'success':
            #print("Votre trajet existe")
            routeLatLons = list(map(router.nodeLatLon, route))
        #else:
            #print("Votre trajet n'existe pas")

        folium.PolyLine(routeLatLons, color="blue", weight=2.5, opacity=1).add_to(idf)
        
        return routeLatLons
    

    def calcul_distance_haversine(self):
        """
        on utilise la distance de haversine
        -----------
        x_A = (latitude, longitude)
        x_B = (latitude, longitude)

        Peu efficace car distance à vol d'oiseau
        """
        self.get_coordo()

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




