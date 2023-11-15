# %% [markdown]
# # Fichier de test du calcul de l'itinéraire optimal
# 
# ## Plan du notebook: 
# 0. Charger les packages utilisés y compris la classe CarNetwork dont on peut retrouver le code dans le fichier CarNetwork.py. 
# 
# 1. Charger les données utilisées (issues du lien "https://www.data.gouv.fr/fr/datasets/r/51606633-fb13-4820-b795-9a2a575a72f1") et les nettoyer à l'aide des méthodes de la classe CarNetwork. 
# 
# 2. Calcul de la distance entre les deux destinations en entrées de la classe CarNetwork. 
# 
# 3. Tester la méthode .trajet_voiture() 

# %% [markdown]
# ### 0. Chargement des packages

# %%
import pandas as pd

# %%
import pyroutelib3 
import os
import sys 

car_network_directory = '/Users/khelifanail/Documents/GitHub/Pycar/Modules'

## si Augustin utilise le chemin absolu est '/Users/augustincablant/Documents/GitHub/Pycar/Modules' 

sys.path.append(car_network_directory)

from CarNetwork import CarNetwork

# %% [markdown]
# ### 1. Chargement des données et nettoyage de celles-ci

# %%
## On initialise un objet de la classe CarNetwork
reseau = CarNetwork('3, rue Dareau, 75014', "5, rue Pierre et Marie Curie, 78120", 30)

# %%
# On nettoie les données à l'aide de la méthode .clean_data()
reseau.clean_data()

# %%
# On affiche les données 
reseau.stations_data.head(3)

# %% [markdown]
# ### 2. Calcul de la distance entre les deux localisations entrées en argument de la classe CarNetwork
# 
# Il est important de calculer cette distance. Cependant, il existe deux manières de calculer cette distance : 
# - à vol d'oiseau 
# - selon les routes existantes
# 
# La distance en vol d'oiseau ne nous intéresse pas, on se déplace en voiture. 
# 
# En revanche, il est important de calculer cette distance selon les routes existances car une voiture dont l'autonomie (entrée en argument de la classe CarNetwork) est supérieure à la distance entre les deux localisations suivant les routes existantes ne nécessite pas de trajet optimisé.
# 
# 

# %%
reseau.get_coordo()

# %%
trajet = reseau.trajet_voiture()

# %% [markdown]
# On note que la variable trajet est une liste dont chaque élément est un tuple de longueur 2 contenant une latitude et une longitude. Ces localisations correspondent aux points succsessifs empruntés par l'utilisaeur lors de son trajet.

# %%
trajet

# %% [markdown]
# On peut représenter le trajet associé à cet itinéraire sur une carte à l'aide de la méthode .get_route_map() codée dans la classe. Cette méthode repose elle-mêne sur la classe **Folium**.

# %%
map1 = reseau.get_route_map()
map1

# %% [markdown]
# On peut désormais calculer la distance associée à cet itinéraire à l'aide de la routine distance_via_routes
# 

# %% [markdown]
# Cette routine renvoie deux éléments : 
# 1. un float *distance* qui renvoie la distance du trajet entre les points A et B.
# 
# 2. une liste de coordonnées (latitude, longitude) qui correspond aux arrêts necessaires pour l'utilisateur résultant de la contrainte d'autonomie du véhicule

# %%
distance, stop_coord = reseau.distance_via_routes()


# %% [markdown]
# La routine .plot_stop_points() permet de visualiser les localisatins contenues dans *stop_coord* (renvoyé comme second argument de reseau).

# %%
reseau.plot_stop_points(map1)

# %%
map1

# %% [markdown]
# plot each time when the autonmy cannot carry

# %%
distance_max = 3
nearest_stations = reseau.nearest_stations(stop_coord, distance_max)

# %%
reseau.plot_nearest_stations(map1, nearest_stations)

# %%
reseau.plot_stations(map1)

# %%
map1


