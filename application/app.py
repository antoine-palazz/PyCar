from flask import Flask, render_template, request
from dash import html
from graphiques import evolution_nbre_voiture_elec
import matplotlib.pyplot as plt
from io import BytesIO
import base64
#from CarNetwork import CarNetwork


app = Flask(__name__)

@app.route('/calcul', methods=['POST'])
def calcul(): 
    """ 
    Permet de calculer et retourner l'itinéraire.
    """
    destination = request.form['destination']
    depart = request.form['depart']
    autonomie = int(request.form['autonomie'])
    message = f"Vous voyagez de {depart} à {destination} avec une autonomie de {autonomie} km."
    return message

@app.route("/next")
def page_suivante1():
    def graph_intro():
        df = evolution_nbre_voiture_elec()
        plt.figure(figsize=(10, 6))
        plt.plot(df['Date'], df['Nombre'], label='Évolution du parc de véhicules électriques en France', color='blue', marker='o')
        plt.xlabel('Date')
        plt.ylabel('Nombre de véhicules électrique en France (x1e6)')
        plt.xticks(rotation=45)  # Rotation des étiquettes de l'axe des x pour rendre les dates plus lisibles
        plt.legend()
        plt.fill_between(df['Date'], df['Nombre'], color='lightgray', alpha=0.7)  # Fond gris clair
        plt.title('Évolution du parc de véhicules électriques en France', fontsize=16)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()  # Pour éviter que les étiquettes de l'axe des x ne se chevauchent
        img_data = BytesIO()  # Conversion du graphique en image base64
        plt.savefig(img_data, format='png')
        img_data.seek(0)
        img_base64 = base64.b64encode(img_data.read()).decode()
        graph_html = f'<img src="data:image/png;base64,{img_base64}" alt="Graphique d\'autonomie">'  # Code HTML pour afficher le graphique
        return graph_html
    get_graph = graph_intro()
    return render_template("evolution_electrique.html", graph = get_graph)

@app.route('/')
def accueil():
    """ 
    Permet d'afficher la page d'accueil.
    """
    return render_template("index.html")


# Lancer l'application avec le terminal
"""
cd #chemin
python app.py
copier le chemin et le coller dans le navigateur
"""
if __name__ == '__main__':
    app.run(debug=True)
