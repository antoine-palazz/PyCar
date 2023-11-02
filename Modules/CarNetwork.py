# Imports 
import pandas as pd
import math
# import googlemaps
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pyroutelib3
from pyroutelib3 import Router
import requests, json
import urllib.parse
import folium 
import geopy.distance


# Coordonnées des villes en France 

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
    --> on précise l'autonomie car si celle-ci est supérieure à la distance totale, 
    alors rien ne sert d'optimiser le trajet.

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
        self.stations_data = pd.read_csv('https://www.data.gouv.fr/fr/datasets/r/517258d5-aee7-4fa4-ac02-bd83ede23d25', sep = ';')

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


    def trajet_voiture(self):
    
        """
        Il faut inclure le code de get_cordo dans le code de cette routine au cas où l'utilisateur 
        utilise la méthode trajet_voiture avant celle get_cordo auquel cas les transformations sur 
        self.x_A et self.x_B n'auraient pas été faites. 
        """
        dep_json_A = requests.get("https://api-adresse.data.gouv.fr/search/?q=" + urllib.parse.quote(self.A) + "&format=json").json()
        dep_json_B = requests.get("https://api-adresse.data.gouv.fr/search/?q=" + urllib.parse.quote(self.B) + "&format=json").json()
        self.x_A = list(dep_json_A['features'][0].get('geometry').get('coordinates'))
        self.x_B = list(dep_json_B['features'][0].get('geometry').get('coordinates'))

        coord_dep = self.x_A 
        coord_arr = self.x_B
        router = pyroutelib3.Router('car')
        depart = router.findNode(coord_dep[1], coord_dep[0])
        #print(depart)
        arrivee = router.findNode(coord_arr[1], coord_arr[0])
        #print(arrivee)

        routeLatLons=[coord_dep,coord_arr]

        status, route = router.doRoute(depart, arrivee)

        if status == 'success':
            #print("Votre trajet existe")
            routeLatLons = list(map(router.nodeLatLon, route))
        #else:
            #print("Votre trajet n'existe pas")

        return routeLatLons
    
    def get_route_map(self):
        trajet = self.trajet_voiture()
        paris_coord = [48.8566, 2.3522]

        # Crée une carte centrée sur Paris
        carte = folium.Map(location=paris_coord, zoom_start=13)

        # Trace l'itinéraire
        folium.PolyLine(locations=trajet, color='red').add_to(carte)

        # Affiche la carte dans le notebook
        return carte
    
    def distance_via_routes(self):

        ## On récupère le trajet en voiture entre les deux destinations 
        # A et B
        trajet = self.trajet_voiture()

        distance = 0

        for i in range(len(trajet)-1):
        
            ## on convertit l'élément i de la liste trajet, 
            # qui est un tuple, en une liste
            trajet_depart = list(trajet[i]) 
            trajet_arrivee = list(trajet[i+1])

            d = geopy.distance.distance(trajet_depart, trajet_arrivee).kilometers

            distance = distance + d
        
        return distance




