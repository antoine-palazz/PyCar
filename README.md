# PyCar

<div style="display: flex; justify-content: space-between;">
    <div style="flex: 1; text-align: right;">
        <picture>
        <source media="(prefers-color-scheme: dark) srcset= "https://github.com/AugustinCablant/PyCar/blob/main/Application/Static/logo.jpeg">
        <source media="(prefers-color-scheme: light)" srcset="https://github.com/AugustinCablant/PyCar/blob/main/Application/Static/logo.jpeg">
        <img alt="Un rapide aperçu" src="https://github.com/AugustinCablant/Projet_python_2A/blob/main/cap.png">
        </picture>
    </div>
    <div style="flex: 1; padding-right: 10px;">
        Projet python de deuxième année à l'ENSAE.
    </div>
    
</div>

## Description du projet 
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

<picture>
 <source media="(prefers-color-scheme: dark)" srcset="https://github.com/AugustinCablant/PyCar/blob/main/images/cap1.png">
 <source media="(prefers-color-scheme: light)" srcset="https://github.com/AugustinCablant/PyCar/blob/main/images/cap1.png">
<img alt="Un rapide aperçu" src="https://github.com/AugustinCablant/PyCar/blob/main/cap.png">
</picture>
<picture>
 <source media="(prefers-color-scheme: dark)" srcset="https://github.com/AugustinCablant/PyCar/blob/main/images/cap2.png">
 <source media="(prefers-color-scheme: light)" srcset="https://github.com/AugustinCablant/PyCar/blob/main/images/cap2.png">
 <img alt="Un rapide aperçu" src="https://github.com/AugustinCablant/PyCar/blob/main/cap.png">
</picture>

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

- Exécuter l'application : python src/main.py
```
$ python Application/main.py
```

## Utilisation

- Accéder à l'interface web à l'adresse : 
```
$ python Application/main.py
```
- Spécifier le point de départ et la destination.
- L'application affichera l'itinéraire optimal avec les bornes de recharge recommandées.

## Contribuer 

Si vous souhaitez contribuer à ce projet, veuillez suivre les étapes suivantes :

- Forker le projet.
- Créer une branche pour votre fonctionnalité : git checkout -b nouvelle-fonctionnalite
- Effectuer les modifications nécessaires.
- Soumettre une demande de fusion (Pull Request).
