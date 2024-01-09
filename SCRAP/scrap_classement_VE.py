# Imports
import urllib
import bs4
import pandas

# from urllib import request
import urllib
import pandas as pd
import re

# URL de la page que nous allons scrapper
url = "https://www.frandroid.com/survoltes/voitures-electriques/1707169_les-70-voitures-electriques-les-plus-vendues-en-france-le-numero-2-mondial-arrive-enfin"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}
request = urllib.request.Request(url, headers=headers)

response = urllib.request.urlopen(request)
data = response.read()

# Récupérer la page HTML correspondante
page = bs4.BeautifulSoup(data, "lxml")

# Nous souhaitons récupérer le classement des voitures électriques
tableau = page.find("table")
tbody = tableau.find("tbody")
tr = tbody.find_all(
    "tr",
)

voitures = []
for i, voiture in enumerate(tr):
    # On veut récupérer uniquement le modèle et non l'immatriculation
    voitures.append(list(voiture)[1].text.strip())

dico = {"Classement": list(range(1, 80)), "Voitures": voitures}
classement = pd.DataFrame(dico)
classement.to_csv("SCRAP/classement_VE_2023.csv")
