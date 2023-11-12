# Imports 
import pandas as pd
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
from geopy.distance import geodesic
from folium.plugins import MousePosition
from folium.plugins import TagFilterButton
from pyproj import Proj, transform

# On importe CarNetwork 

from CarNetwork import CarNetwork

class Autoroute(CarNetwork):

    def __init__(self, A, B, autonomie):
        super().__init__(A, B, autonomie)
        self.stations_péages = pd.read_csv('https://static.data.gouv.fr/resources/gares-de-peage-du-reseau-routier-national-concede/20230728-163544/gares-peage-2023.csv', sep = ';')

    
    def clean_base(self):

        ## Dans la base de donnée, les coordonnées des péages sont en 
        #  unité de Lambert 93. Nous les transformons en degrés géographique

        ## Dans la base de donnée, les coordonées de Lambert données dans 
        #  les colonnes 'x' et 'y' sont des strings, on corrige ça 

        self.stations_péages['x'] = self.stations_péages['x'].astype(str).str.replace(',', '.').astype(float)
        self.stations_péages['y'] = self.stations_péages['y'].astype(str).str.replace(',', '.').astype(float)


        def lambert93_to_latlon(x, y):

            in_proj = Proj(init='epsg:2154')  # EPSG code for Lambert 93
            out_proj = Proj(init='epsg:4326')  # EPSG code for WGS84 (lat/lon)

            lon, lat = transform(in_proj, out_proj, x, y)
            return lat, lon
                
        ## On crée deux nouvelles colonnes 
        self.stations_péages['xlongitude'] = lambert93_to_latlon(self.stations_péages['x'].str.replace(',', '.').astype(float), self.stations_péages['y'].str.replace(',', '.').astype(float))[0]
        self.stations_péages['ylatitude'] = lambert93_to_latlon(self.stations_péages['x'].str.replace(',', '.').astype(float), self.stations_péages['y'].str.replace(',', '.').astype(float))[1]

        ## On renomme les colonnes par soucis de clarté
        self.stations_péages.rename(columns={'x': 'lambert93_x', 'y' : 'lambert93_y'}, inplace=True)

        '''
        Les coordonnées de longitude > 90 ou de latitude > 90 sont inutiles car elles dépassent les limites 
        des valeurs possibles pour la longitude (de -180 à 180) et la latitude (de -90 à 90) sur la surface 
        de la Terre, et donc, elles sont généralement considérées comme des données incorrectes. 
        La routine supprime ces données du dataframe.
        '''


        liste = []
        for row in self.stations_péages.itertuples():

            if row.xlongitude > 90 or row.ylatitude > 90:
                liste.append(row.Index)

        self.stations_péages.drop(liste)