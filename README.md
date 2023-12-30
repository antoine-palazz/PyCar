# PyCar

<div style="display: flex; justify-content: space-between;">
    <div style="flex: 1; text-align: right;">
        <picture>
        <source media="(prefers-color-scheme: dark) srcset= "https://github.com/AugustinCablant/PyCar/blob/main/Application/Static/logo.jpeg">
        <source media="(prefers-color-scheme: light)" srcset="https://github.com/AugustinCablant/PyCar/blob/main/Application/Static/logo.jpeg">
        <img alt="Un rapide aperçu" src="https://github.com/AugustinCablant/PyCar/blob/main/Application/Static/logo.jpeg">
        </picture>
    </div>
    <div style="flex: 1; padding-right: 10px;">
        Projet python de deuxième année à l'ENSAE.
    </div>
    
</div>

## But 
Ce projet a pour objectif de créer un itinéraire optimal pour un véhicule électrique en tenant compte des bornes de recharge disponibles sur le territoire français. L'idée est d'optimiser le trajet en minimisant les arrêts de recharge et en maximisant l'efficacité énergétique du parcours.

Collaborateurs : 
- Naïl Khelifa 
- Thomas Pogu
- Augustin Cablant

## Description du projet 
Recherche d'Itinéraire : Le système permet à l'utilisateur de spécifier un point de départ et une destination, puis calcule l'itinéraire optimal en considérant les bornes de recharge électrique le long du trajet.

Informations sur les Bornes de Recharge : Le système fournit des informations détaillées sur les bornes de recharge disponibles, y compris leur emplacement, le type de connecteur, la puissance de recharge, etc.

Optimisation de l'Énergie : L'algorithme d'optimisation prend en compte la capacité de la batterie du véhicule, les conditions de circulation et la disponibilité des bornes de recharge pour maximiser l'efficacité énergétique du trajet.

## Architecture du répertoire 
Les principaux dossiers sont : 
- Notebooks : qui contient tous les notebooks nous ayant permis de visualiser les données.
- SCRAP : qui contient les codes qui nous ont permis de scrapper plusieurs pages internet.
- Application : contient la web-application que nous avons conçu pour visualiser les itinéraires.

## Technologies utilisées
- Langage de Programmation : Python
- Framework Web : Flask (pour une interface utilisateur)

## Structure du projet

- Le dossier notebooks contient tous les notebooks de statistiques descriptives (présents dans le dossier notebooks_unique). Nous avons fait le choix de tout regrouper dans le fichier EDA.ipynb. 
#### Le fichier [EDA.ipynb](https://github.com/AugustinCablant/PyCar/blob/main/notebooks/EDA.ipynb) est construit de la manière suivante :
- ##### I. La pollution en France

- ##### II. Répartition de la population en France métropolitaine

- ##### III. Répartition des véhicules électriques en France métropolitaine

- ###### III.B Analyse du fichier
- ###### III.C Répartition des ventes de véhicules en fonction de leur motorisation en France
- ###### III.D Classement des véhicules électriques en France métropolitaine
- ###### III.E Autonomie des voitures électriques
- ###### III.F Évolution des voitures électriques en France métropolitaine
- ###### III.G Voitures particulières immatriculées par commune et par type de recharge
- ###### III.H Projection de ventes de voitures électriques selon l'IEA
- ###### III.I Tentative de prédictions

- ##### IV. Répartition des bornes électriques en France métropolitaine

- ##### V. Accidents en France métropolitaine

- DOWNLOAD est le dossier avec les datasets téléchargés
- Modules est le dossier contenant la classe permettant de trouver l'itinéraire optimal
- SCRAP est le dossier contenant les codes pour scraper les données ainsi que les datasets correspondants

## Installation

- Cloner le dépôt : 
```
$ git clone https://github.com/AugustinCablant/PyCar.git
```

- Installer les dépendances :

```
$ pip install -r requirements.txt
```

- Exécuter l'application : python Application/app.py
```
$ python Application/main.py
```

## Utilisation

- Accéder à l'interface web à l'adresse : 
```
$ python Application/app.py
``` 
<picture>
 <source media="(prefers-color-scheme: dark)" srcset="https://github.com/AugustinCablant/PyCar/blob/main/images/python.png">
 <source media="(prefers-color-scheme: light)" srcset="https://github.com/AugustinCablant/PyCar/blob/main/images/python.png">
 <img alt="Un rapide aperçu" src="https://github.com/AugustinCablant/PyCar/blob/main/images/python.png">
</picture>
<picture>
 <source media="(prefers-color-scheme: dark)" srcset="https://github.com/AugustinCablant/PyCar/blob/main/images/web_app.png">
 <source media="(prefers-color-scheme: light)" srcset="https://github.com/AugustinCablant/PyCar/blob/main/images/web_app.png">
 <img alt="Un rapide aperçu" src="https://github.com/AugustinCablant/PyCar/blob/main/images/web_app.png">
</picture>

Vous pouvez accéder à l'Exploratory Data Analysis que nous avons effectué en cliquant sur l'onglet "EDA"
<picture>
 <source media="(prefers-color-scheme: dark)" srcset="https://github.com/AugustinCablant/PyCar/blob/main/images/EDA.png">
 <source media="(prefers-color-scheme: light)" srcset="https://github.com/AugustinCablant/PyCar/blob/main/images/EDA.png">
 <img alt="Un rapide aperçu" src="https://github.com/AugustinCablant/PyCar/blob/main/images/EDA.png">
</picture>

Ou bien retrouver ce qui a motivé ce projet en cliquant sur "Pourquoi ce projet ?"
<picture>
 <source media="(prefers-color-scheme: dark)" srcset="https://github.com/AugustinCablant/PyCar/blob/main/images/Pourquoi%20%3F.png">
 <source media="(prefers-color-scheme: light)" srcset="https://github.com/AugustinCablant/PyCar/blob/main/images/Pourquoi%20%3F.png">
 <img alt="Un rapide aperçu" src="https://github.com/AugustinCablant/PyCar/blob/main/images/Pourquoi%20%3F.png">
</picture>

- Spécifier le point de départ et la destination.
<picture>
 <source media="(prefers-color-scheme: dark)" srcset="https://github.com/AugustinCablant/PyCar/blob/main/images/web_app_1.png">
 <source media="(prefers-color-scheme: light)" srcset="https://github.com/AugustinCablant/PyCar/blob/main/images/web_app_1.png">
 <img alt="Un rapide aperçu" src="https://github.com/AugustinCablant/PyCar/blob/main/images/web_app_1.png">
</picture>
- L'application affichera l'itinéraire optimal avec les bornes de recharge recommandées.
<picture>
 <source media="(prefers-color-scheme: dark)" srcset="https://github.com/AugustinCablant/PyCar/blob/main/images/iti.png">
 <source media="(prefers-color-scheme: light)" srcset="https://github.com/AugustinCablant/PyCar/blob/main/images/iti.png">
 <img alt="Un rapide aperçu" src="https://github.com/AugustinCablant/PyCar/blob/main/images/iti.png">
</picture>

## Contribuer 

Si vous souhaitez contribuer à ce projet, veuillez suivre les étapes suivantes :

- Forker le projet.
- Créer une branche pour votre fonctionnalité : git checkout -b nouvelle-fonctionnalite
- Effectuer les modifications nécessaires.
- Soumettre une demande de fusion (Pull Request).

## Bibliographie des sources

### Notebook accidents_2022_idf.ipynb

- [Observatoire national interministériel de la sécurité routière](https://www.onisr.securite-routiere.gouv.fr/sites/default/files/2023-10/ONISR_DDT_2022.xlsx), *Accidents de voiture sur l'année 2022*, 2022 : fichier excel (seul moyen d'accès) "Accidents_2022_idf.xlsx" (DOWNLOADS)

### Fichier CarNetwork.py 

- [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/bornes-de-recharge-pour-vehicules-electriques-3/), *Bornes de recharge pour véhicules électriques*, 2019 (Version la plus récente).

- [adresse.data.gouv.fr](https://adresse.data.gouv.fr/api-doc/adresse), *API Adresse*.

- [France GeoJson](https://france-geojson.gregoiredavid.fr/), *France GeoJson* : utilisé pour obtenir les coordonnées GeoJson des limites de l'Île-de-France

### Fichier Graphique.py

- [INSEE](https://www.insee.fr/fr/statistiques/fichier/2015759/deve-envir-emissions-co2.xlsx), *Émissions de gaz à effet de serre par activité*

- [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/bornes-de-recharge-pour-vehicules-electriques-3/), *Bornes de recharge pour véhicules électriques*, 2019 (Version la plus récente).

### Fichier autonomie_km.py

- [International Energy Agency](https://www.iea.org/data-and-statistics/charts/average-price-and-driving-range-of-bevs-2010-2019), *Average price and driving range of BEVs, 2010-2019*

### Différents scraps utiles

  -[Etat des lieux des voitures électriques en France](https://fr.wikipedia.org/wiki/Voiture_%C3%A9lectrique_en_France) *Page Wikipédia présentant le parc des véhicules électriques en France (version la plus récente)*

  -[Accidents principaux en France](https://fr.wikipedia.org/wiki/%C3%89volution_d%C3%A9taill%C3%A9e_des_accidents_routiers_en_France_m%C3%A9tropolitaine) *Page Wikipédia présentant les accidents principaux en France (version la plus récente)*

  -[Liste de différentes autonomies de véhicules électriques](https://www.automobile-propre.com/voiture-electrique-top-des-meilleures-autonomies/) *Site présentant les véhciules électriques ainsi que leurs autonomies, (version la plus récente)*

  -[Classement des véhiucules électriques les plus vendues ](https://www.frandroid.com/survoltes/voitures-electriques/1707169_les-70-voitures-electriques-les-plus-vendues-en-france-le-numero-2-mondial-arrive-enfin) *Site présentant les véhicules électriques les plus vendus en 2023 (version la plus récente)*
 



## Remarques 

On trouvera dans le notebook **test1.ipynb** (fichier Tests) un mode d'emploi de la classe derrière notre projet. 
