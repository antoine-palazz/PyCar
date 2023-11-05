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
        distance_1 = 0 ## we use this double variable in the if
        # condition to remove the autonomy

        stop_coord = []

        for i in range(len(trajet)-1):
        
            ## on convertit l'élément i de la liste trajet, 
            # qui est un tuple, en une liste
            trajet_depart = list(trajet[i]) 
            trajet_arrivee = list(trajet[i+1])

            d = geopy.distance.distance(trajet_depart, trajet_arrivee).kilometers

            distance = distance + d
            distance_1 = distance

            ## On fait d'une pierre deux coup dans ce code en calculant 
            #  une liste qui renvoie les premiers points à partir desquels 
            #  l'autonomie ne couvre plus la distance. 

            if self.autonomie < distance_1:
                stop_coord.append(trajet[i])
                distance_1 = distance - self.autonomie

        
        return distance, stop_coord
    
    def plot_stop_points(self, map):

        distance, stop_coord = self.distance_via_routes()


        for i in range(len(stop_coord)):
            lat = stop_coord[i][0]
            lon = stop_coord[i][1]

            folium.Marker(location=[lat, lon], icon=folium.Icon(color='purple')).add_to(map)



    def plot_stations(self, map):

        df = self.stations_data

        # we clean the dataframe 

        droping_liste = list(set(df[df['xlongitude'].isna()].index.to_list() + df[df['ylatitude'].isna()].index.to_list()))
        df.drop(droping_liste, inplace = True)

        # we transform the acces row in the dataframe by defining 
        # a function that we will then apply to the "acces_recharge" row

        def transform_acces(row):
            if not pd.isna(row):  # On ne peut rien dire des nan
                row = row.lower()  # Mettre en lettre minuscule 
                mots = row.split(' ')
                if 'payant' in mots: row = 'payant'
                elif 'gratuit' in mots: row = 'gratuit'
                for mot in mots: 
                    if len(mot.split('€'))>1: row = 'payant'
                    if mot=='carte' or mot=='badge': row = 'carte ou badge'
                    if mot=='oui': row = 'information manquante'
                #else: row = 'accès spécial'
            else: row = 'information manquante'
            return row
        
        df['acces_recharge'] = df['acces_recharge'].apply(transform_acces)
        list(df['acces_recharge'].unique())

        legend_html = """
        <div style="position: fixed; 
                    top: 10px; 
                    right: 10px; 
                    width: 220px; 
                    background-color: rgba(255, 255, 255, 0.8); 
                    border: 2px solid #000; 
                    border-radius: 5px; 
                    box-shadow: 3px 3px 5px #888; 
                    z-index: 1000; padding: 10px; font-size: 14px; font-family: Arial, sans-serif;">
            <p style="text-align: center; font-size: 18px;"><strong>Légende de la Carte</strong></p>
            
            <p><i class="fa fa-map-marker" style="color: orange;"></i> <strong>Marqueur Rouge</strong>: Payant</p>
            
            <p><i class="fa fa-map-marker" style="color: green;"></i> <strong>Marqueur Bleu</strong>: Gratuit</p>
            
            <p><i class="fa fa-circle" style="color: grey; font-size: 20px;"></i> <strong>Point Vert</strong>: Information manquantes</p>
            
            <p><i class="fa fa-square" style="color: cyan; font-size: 20px;"></i> <strong>Carré Orange</strong>: Carte ou badge</p>
            
            <p><i class="fa fa-circle" style="color: yellow; font-size: 20px;"></i> <strong>Point Violet</strong>: Charges gratuites</p>
            
            <p><i class="fa fa-star" style="color: purple; font-size: 20px;"></i> <strong>Étoile Dorée</strong>: Points d'arrêt</p>
        </div>
        """

        # Ajoutez la légende personnalisée à la carte
        map.get_root().html.add_child(folium.Element(legend_html))


        for index, lat, lon, com, acces_recharge in df[['ylatitude', 'xlongitude', 'n_station', 'acces_recharge']].itertuples():
            # Créez un marqueur avec une couleur différente en fonction des valeurs
            if acces_recharge == 'payant': fill_color = 'orange'
            elif acces_recharge == 'gratuit': fill_color = 'green'
            elif acces_recharge == 'information manquante': fill_color = 'grey'
            elif acces_recharge == 'carte ou badge': fill_color = 'cyan'
            elif acces_recharge == 'charges gratuites de 12 à 14h et de 19h à 21h': fill_color = 'yellow'

            # Ajoutez le marqueur à la carte
            folium.RegularPolygonMarker(location=[lat, lon], popup=com, fill_color=fill_color, color =fill_color, radius=5).add_to(map)



