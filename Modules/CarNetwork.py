# Imports 
import pandas as pd
import math
from geopy.distance import geodesic
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
import plotly.express as px
from fonctions import trajet, recherche_station_proche, trajet, trajet_electrique, coor_cp, clean_df

# Coordonnées des villes en France 
URL = "https://www.data.gouv.fr/fr/datasets/r/51606633-fb13-4820-b795-9a2a575a72f1"
df = pd.read_csv(URL)

# Bornes 
URL = 'https://www.data.gouv.fr/fr/datasets/r/517258d5-aee7-4fa4-ac02-bd83ede23d25'
df_bornes = pd.read_csv(URL, sep = ';')
df_bornes.apply(clean_df, inplace = True)

#Code postaux
df_code = pd.read_csv('https://www.data.gouv.fr/fr/datasets/r/dbe8a621-a9c4-4bc3-9cae-be1699c5ff25')


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
        Permet de récupérer la latitude et la longitude [latitude,longitude]
        """
        dep_json_A = requests.get("https://api-adresse.data.gouv.fr/search/?q=" + urllib.parse.quote(self.A) + "&format=json").json()
        dep_json_B = requests.get("https://api-adresse.data.gouv.fr/search/?q=" + urllib.parse.quote(self.B) + "&format=json").json()
        self.x_A = list(dep_json_A['features'][0].get('geometry').get('coordinates'))
        self.x_B = list(dep_json_B['features'][0].get('geometry').get('coordinates'))

    def visu_iti(self):
        départ = coor_cp(df_code, self.A)  # [lat, lon]
        if départ == None:
            return "Adresse de départ incorrecte"

        fin = coor_cp(df_code, self.B)
        if fin == None:
            return "Adresse d'arrivée incorrecte"

        Trajet_thermique_lat, Trajet_thermique_lon, total_thermique = trajet(départ, fin)
        Type = ['Thermique']*len(Trajet_thermique_lat)

        elec = trajet_electrique(Trajet_thermique_lat, Trajet_thermique_lon, self.autonomie)
        if elec == None:
            return 'Autonomie insuffisante'

        Trajet_lat_elec, Trajet_lon_elec, total_elec = elec
        Type_elec = ['Electrique']*len(Trajet_lat_elec)
        Type += Type_elec

        Trajet_lat = Trajet_thermique_lat + Trajet_lat_elec
        Trajet_lon = Trajet_thermique_lon + Trajet_lon_elec
        data = pd.DataFrame({'Latitude': Trajet_lat, 'Longitude': Trajet_lon, 'Type': Type})
        fig = px.line_mapbox(data, lat='Latitude',
                            lon='Longitude',
                            color='Type', 
                            mapbox_style='open-street-map', 
                            height=800)
        return fig, total_thermique, total_elec


    def trajet_voiture(self):
        '''
        - permet de renvoyer le trajet de voiture emprunté pour relier les points A et B 
        '''

        coor_depart = [self.x_A[1], self.x_A[0]]     # faire attention au petit remaniement du début
        coor_arrivee = [self.x_B[1], self.x_B[0]]

        router = Router("car")
        depart = router.findNode(coor_depart[0], coor_depart[1])
        #print(depart)
        arrivee = router.findNode(coor_arrivee[0], coor_arrivee[1])
        #print(arrivee)

        routeLatLons=[coor_depart,coor_arrivee]
        
        status, route = router.doRoute(depart, arrivee)
        if status == 'success':
            print("Votre trajet existe")
            routeLatLons = list(map(router.nodeLatLon, route))
        else:
            print("Votre trajet n'existe pas")
        return routeLatLons


"""
def nearest_station(self):
    stations = data[['x_longitude', 'y_latitude']]
    coord_actuelle = np.array([self.position_actuelle[0], self.position_actuelle[1]])
    distances = distance.cdist(coord_actuelle, stations, metric='euclidean')
    indice_min_distance = np.argmin(distances)
    nearest_station = stations.iloc[indice_min_distance][['x_longitude', 'y_latitude']]

    return nearest_station  
"""




