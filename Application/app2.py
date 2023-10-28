from flask import Flask,render_template,request
import pickle
import numpy as np
app = Flask('__name__')
from dash import html
from graphiques import evolution_nbre_voiture_elec
import matplotlib.pyplot as plt
from io import BytesIO
import base64
#from CarNetwork import CarNetwork


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

""" 

@app.route('/predict',methods=["POST"])
def predict():
    feature=[int(x) for x in request.form.values()]
    feature_final=np.array(feature).reshape(-1,1)
    prediction=model.predict(feature_final)
    return render_template('index.html',prediction_text='Price of House will be Rs. {}'.format(int(prediction)))
"""

@app.route('/calcul', methods=['POST'])
def calcul():
    destination = request.form['destination']
    depart = request.form['depart']
    autonomie = int(request.form['autonomie'])
    
    # Ici, vous pouvez effectuer le calcul d'autonomie en fonction des données fournies

    # Par exemple, un simple exemple de calcul :
    message = f"Vous voyagez de {depart} à {destination} avec une autonomie de {autonomie} km."
    return message

if(__name__=='__main__'):
    app.run(debug=True)