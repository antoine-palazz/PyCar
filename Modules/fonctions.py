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
import folium 

# Bornes 
URL = 'https://www.data.gouv.fr/fr/datasets/r/517258d5-aee7-4fa4-ac02-bd83ede23d25'
df_bornes = pd.read_csv(URL, sep = ';')

def clean_df(dataframe):
    liste = []
    for row in dataframe.itertuples():
        if row.xlongitude > 90 or row.ylatitude > 90:
            liste.append(row.Index)
    df_bornes = dataframe.drop(liste)
    droping_liste = list(set(df_bornes[df_bornes['xlongitude'].isna()].index.to_list() + df_bornes[df_bornes['ylatitude'].isna()].index.to_list()))
    df = df_bornes.drop(liste)
    return df

def coor_cp(df_code, code_postale):
    for row in df_code.itertuples():
        cp = row.code_postal
        if code_postale == cp:
            lat = row.latitude
            lon = row.longitude
            return [lat, lon]
    return None

def trajet(départ, fin):
        """ 
        Retourne une liste de longitude et 
        de latitude correspondant à la route à suivre pour 
        rejoindre fin depuis départ définis à partir de leur coordonées respectives
        """
        Trajet_lat = []
        Trajet_lon = []
        total = 0
        router = Router('car')
        start = router.findNode(départ[0], départ[1])
        end = router.findNode(fin[0], fin[1])
        status, route = router.doRoute(start, end)
        if status == 'success':
            routeLatLons = list(map(router.nodeLatLon, route))
            for elem in routeLatLons:
                lat, lon = elem
                Trajet_lat.append(lat)
                Trajet_lon.append(lon)
        for i in range(len(Trajet_lat)-1):
            lat_i = Trajet_lat[i]
            lat_f = Trajet_lat[i+1]
            lon_i = Trajet_lon[i]
            lon_f = Trajet_lon[i+1]
            d = geodesic((lat_i, lon_i), (lat_f, lon_f)).km
            total += d
        return Trajet_lat, Trajet_lon, total

def recherche_station_proche(df, dist, lat, lon):
        """ 
        Recherche la station la plus proche dans un périmètre de rayon dist et de centre de coordonnées lat, lon
        """
        lat, lon = np.float(lat), np.float(lon)
        lowest = [0, dist+10]  # index, min distance
        dataframe0 = df.dropna(subset = ['xlongitude', 'ylatitude'])
        index = 0
        for row in dataframe0.itertuples():
            lat_s = row.ylatitude
            lon_s = row.xlongitude
            d = geodesic((lat, lon), (lat_s, lon_s)).km
            if lowest[1] > d:
                lowest[1] = d
                lowest[0] = index
            index += 1

        if lowest[1] > dist:
            return None
        else:
            index = lowest[0]
            ligne = dataframe0.iloc[[index]]
            lat = ligne['ylatitude'].values[0]
            lon = ligne['xlongitude'].values[0]
            nom = ligne['n_enseigne'].values[0]
            return lat, lon, nom
        
def trajet(départ, fin):
    """ 
    Retourne une liste de longitude et 
    de latitude correspondant à la route à suivre pour 
    rejoindre fin depuis départ définis à partir de leur coordonées respectives
    """
    Trajet_lat = []
    Trajet_lon = []
    total = 0
    router = Router('car')
    start = router.findNode(départ[0], départ[1])
    end = router.findNode(fin[0], fin[1])
    status, route = router.doRoute(start, end)
    if status == 'success':
        routeLatLons = list(map(router.nodeLatLon, route))
        for elem in routeLatLons:
            lat, lon = elem
            Trajet_lat.append(lat)
            Trajet_lon.append(lon)
    for i in range(len(Trajet_lat)-1):
        lat_i = Trajet_lat[i]
        lat_f = Trajet_lat[i+1]
        lon_i = Trajet_lon[i]
        lon_f = Trajet_lon[i+1]
        d = geodesic((lat_i, lon_i), (lat_f, lon_f)).km
        total += d
    return Trajet_lat, Trajet_lon, total
        
def trajet_electrique(Trajet_thermique_lat, Trajet_thermique_lon, autonomie):
    """ 
    Pour les véhicules électriques
    """
    Trajet_lat = []
    Trajet_lon = []
    parcourue = 0
    total = 0
    router = Router('car')
    for k in range(len(Trajet_thermique_lat)-1):
        if parcourue <= autonomie*0.7:
            lat_i = Trajet_thermique_lat[k]
            lat_f = Trajet_thermique_lat[k+1]
            lon_i = Trajet_thermique_lon[k]
            lon_f = Trajet_thermique_lon[k+1]

            start = router.findNode(lat_i, lon_i)
            end = router.findNode(lat_f, lon_f)
            status, route = router.doRoute(start, end)
            if status == 'success':
                routeLatLons = list(map(router.nodeLatLon, route))
                for i in range(len(routeLatLons)-1):
                    dep_lat = routeLatLons[i][0]
                    dep_lon = routeLatLons[i][1]
                    fin_lat = routeLatLons[i+1][0]
                    fin_lon = routeLatLons[i+1][1]
                    Trajet_lat.append(dep_lat)
                    Trajet_lat.append(fin_lat)
                    Trajet_lon.append(dep_lon)
                    Trajet_lon.append(fin_lon)
                    d = geodesic((dep_lat, dep_lon), (fin_lat, fin_lon)).km
                    parcourue += d
        else:
            station = recherche_station_proche(df_bornes, autonomie*0.3, Trajet_thermique_lat[k], Trajet_thermique_lon[k])
            if station == None:
                return None
            else:
                lat, lon, nom = station
                start = router.findNode(
                    Trajet_thermique_lat[k], Trajet_thermique_lon[k])
                end = router.findNode(lat, lon)
                status, route = router.doRoute(start, end)
                if status == 'success':
                    routeLatLons = list(map(router.nodeLatLon, route))
                    for i in range(len(routeLatLons)-1):
                        dep_lat = routeLatLons[i][0]
                        dep_lon = routeLatLons[i][1]
                        fin_lat = routeLatLons[i+1][0]
                        fin_lon = routeLatLons[i+1][1]
                        Trajet_lat.append(dep_lat)
                        Trajet_lat.append(fin_lat)
                        Trajet_lon.append(dep_lon)
                        Trajet_lon.append(fin_lon)
                        d = geodesic((dep_lat, dep_lon), (fin_lat, fin_lon)).km
                        parcourue += d
                start = router.findNode(fin_lat, fin_lon)
                end = router.findNode(Trajet_thermique_lat[k], Trajet_thermique_lon[k])
                status, route = router.doRoute(start, end)
                if status == 'success':
                    routeLatLons = list(map(router.nodeLatLon, route))
                    for i in range(len(routeLatLons)-1):
                        dep_lat = routeLatLons[i][0]
                        dep_lon = routeLatLons[i][1]
                        fin_lat = routeLatLons[i+1][0]
                        fin_lon = routeLatLons[i+1][1]
                        Trajet_lat.append(dep_lat)
                        Trajet_lat.append(fin_lat)
                        Trajet_lon.append(dep_lon)
                        Trajet_lon.append(fin_lon)
                        d = geodesic((dep_lat, dep_lon), (fin_lat, fin_lon)).km
                        parcourue += d
            total += parcourue
            parcourue = 0
    total += parcourue
    return Trajet_lat, Trajet_lon, total