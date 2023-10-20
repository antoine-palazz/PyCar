# Imports
import urllib
import bs4
import pandas
from urllib import request
import pandas as pd
import re

# URL de la page que nous allons scrapper 
url = 'https://fr.wikipedia.org/wiki/Voiture_%C3%A9lectrique_en_France'
request_text = request.urlopen(url).read()

# Récupérer la page HTML correspondante 
page = bs4.BeautifulSoup(request_text, "lxml")

# Nous souhaitons récupérer le tableau des statistiques d'immatriculation 
tableau = page.find("table", {'class' : 'wikitable center'})  

# Récupérer le 'tbody'
tableau_tbody = tableau.find('tbody')

# Récupérer tous les 'tr'
tableau_tr = tableau_tbody.find_all('tr')

# On commence par récupérer les colonnes de notre futur dataframe
colonnes = []
for element in tableau_tr[0].find_all('th'):
    colonnes.append(element.text.strip())

row = []
# On récupère les informations correspondantes
for i, donnees in enumerate(tableau_tr):
    if i>0:
        recup = donnees.find_all('td')
        for j, element in enumerate(recup):
            row.append(element.text.strip())

# Un peu de remise en forme des données
valeurs = [[element.split('[')[0] for element in row[::4]], 
           [''.join(re.findall(r'\d+', element.split('[')[0])) for element in row[1::4]],
           [(element.split('[')[0]).replace('\xa0', '') for element in row[2::4]], 
           [(element.split('[')[0]).replace('\xa0', '') if element!='' else element for element in row[3::4] ]]
dico = dict(zip(colonnes,valeurs))

# Évolution des voitures électriques sous forme de dataframe
EVOL_VE = pd.DataFrame(dico)
EVOL_VE.to_csv('SCRAP/EVOL_VE.csv')  

# ******* # ******* # ******* # ******* # ******* # ******* # ******* # ******* # ******* # ******* # ******* #

# Sur la même page wikipédia on scrap la répartition géographique des ventes de véhicules particuliers 100 % électriques en France en 2018
# On adopte la même démarche
tableau2 = page.find("table", {'class' : 'sortable wikitable center'})   
tableau_tbody = tableau2.find('tbody') 
tableau_tr = tableau_tbody.find_all('tr')

colonnes2 = []
for mot in tableau_tr[0]:
    if mot.text.strip()!='':
        colonnes2.append(mot.text.strip())

row2 = []
for i, donnees in enumerate(tableau_tr):
    if i>0:
        recup = donnees.find_all('td')
        for j, element in enumerate(recup):
            row2.append(element.text.strip())

valeurs2 = [[element for element in row2[:len(row2)-1:3]], 
           [element.replace('\xa0', '') for element in row2[1::3]],
           [element.replace('\xa0', '') for element in row2[2::3]]]

dico2 = dict(zip(colonnes2,valeurs2))
VE_2018 = pd.DataFrame(dico2)
VE_2018.drop(17, inplace=True)  #la ligne Total nous est inutile
VE_2018.to_csv('SCRAP/VE_2018.csv')