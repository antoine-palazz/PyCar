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

    def __init__(self):
        super().__init__()
        self.stations_péages = pd.read_csv('https://static.data.gouv.fr/resources/gares-de-peage-du-reseau-routier-national-concede/20230728-163544/gares-peage-2023.csv', sep = ';')

    
    def clean_base():

        ## Dans la base de donnée, les coordonnées des péages sont en 
        #  unité de Lambert 93. Nous les transformons en degrés géographique

        def lambert93_to_latlon(x, y):

            in_proj = Proj(init='epsg:2154')  # EPSG code for Lambert 93
            out_proj = Proj(init='epsg:4326')  # EPSG code for WGS84 (lat/lon)

            lon, lat = transform(in_proj, out_proj, x, y)
            return lat, lon
                
        df


