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

# On importe CarNetwork 

from CarNetwork import CarNetwork

class Autoroute(CarNetwork):

    def __init__(self):
        super().__init__()
        self.stations_péages = pd.read_csv('https://static.data.gouv.fr/resources/gares-de-peage-du-reseau-routier-national-concede/20230728-163544/gares-peage-2023.csv', sep = ';')

    





