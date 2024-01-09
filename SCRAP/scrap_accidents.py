# Imports
import urllib
import bs4
import pandas
from urllib import request
import pandas as pd
import re

# URL de la page que nous allons scrapper
url = "https://fr.wikipedia.org/wiki/%C3%89volution_d%C3%A9taill%C3%A9e_des_accidents_routiers_en_France_m%C3%A9tropolitaine"
request_text = request.urlopen(url).read()

# Récupérer la page HTML correspondante
page = bs4.BeautifulSoup(request_text, "lxml")

# Nous souhaitons récupérer le tableau de l'évolution des accidents
tableau = page.find("table", {"class": "wikitable"})

# De 1948 à 1967
# Récupérer le 'tbody'
tableau_tbody = tableau.find("tbody")

# Récupérer tous les 'tr'
tableau_tr = tableau_tbody.find_all("tr")

# Récupération des colonnes de notre futur dataframe
colonnes = []
for element in tableau_tr[0].find_all("th"):
    colonnes.append(element.text.strip())

colonnes = colonnes[0:2]
colonnes = [el.split("[")[0] for el in colonnes]
row = []
# On récupère les informations correspondantes
for i, donnees in enumerate(tableau_tr):
    if i > 0:
        recup = donnees.find_all("td")[0:2]
        for j, element in enumerate(recup):
            row.append(element.text.strip())

valeurs = [element.replace("\xa0", "") for element in row]
n = len(valeurs)
values = [[valeurs[2 * k], valeurs[2 * k + 1]] for k in list(range(int(n / 2)))]


# De 1967 à 2004
tableau2 = page.findAll("table", {"class": "wikitable"})
tableau_tbody2 = tableau2[1].find("tbody")
tableau_tr2 = tableau_tbody2.find_all("tr")
row2 = []
# On récupère les informations correspondantes
for i, donnees in enumerate(tableau_tr2):
    if i > 0:
        recup = donnees.find_all("td")[0:2]
        for j, element in enumerate(recup):
            row2.append(element.text.strip())
valeurs2 = [element.replace("\xa0", "") for element in row2]
n2 = len(valeurs2)
values2 = [[valeurs2[2 * k], valeurs2[2 * k + 1]] for k in list(range(int(n2 / 2)))]
values += values2

# De 2004 à 2022
tableau_tbody3 = tableau2[2].find("tbody")
tableau_tr3 = tableau_tbody3.find_all("tr")
row3 = []
for i, donnees in enumerate(tableau_tr3):
    if i > 0:
        recup = donnees.find_all("td")[0:2]
        for j, element in enumerate(recup):
            row3.append(element.text.strip())

valeurs3 = [element.replace("\xa0", "") for element in row3]
n3 = len(valeurs3)
values3 = [
    [valeurs3[2 * k].split("[")[0], valeurs3[2 * k + 1]]
    for k in list(range(int(n3 / 2)))
]
values += values3
####


# DataFrame Évolution des accidents
EVOL_ACC = pd.DataFrame(values, columns=colonnes).set_index("Année")
EVOL_ACC.to_csv("SCRAP/EVOL_ACC.csv")
