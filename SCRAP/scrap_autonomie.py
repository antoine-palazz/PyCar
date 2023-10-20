# Imports
import urllib
import bs4
import pandas
#from urllib import request
import urllib
import pandas as pd
import re

# URL de la page que nous allons scrapper 
url = 'https://www.automobile-propre.com/voiture-electrique-top-des-meilleures-autonomies/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
request = urllib.request.Request(url, headers=headers)

response = urllib.request.urlopen(request)
data = response.read()

# Récupérer la page HTML correspondante 
page = bs4.BeautifulSoup(data, "lxml")
print(page)

# Nous souhaitons récupérer le classement des voitures électriques
tableau = page.find("table", {'class' : "table table-1000km"}) 
tbody = tableau.find('tbody')
tr = tbody.find_all('tr', {'class' : "parent"})
classement = []
voiture = []
kWh = []
prix = []
autonomie = []
for t in tr:
    liste = t.text.split('\n')
    classement.append(liste[1])
    voiture.append(liste[2])
    kWh.append(liste[4])
    prix.append(liste[5])
    autonomie.append(liste[6])

dico = {'Classement': classement,
        'Voitures': voiture,
         'kWh' : kWh,
          'Prix' : prix, 
           'Autonomie': autonomie }

autonomie = pd.DataFrame(dico)
autonomie.set_index('Classement', inplace = True)
autonomie.to_csv('SCRAP/autonomie_VE.csv')
