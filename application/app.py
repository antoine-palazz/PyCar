from flask import Flask


app = Flask(__name__)

@app.route('/')
def accueil():
    return '''
    <html>
    <head>
        <title>Calcul d'autonomie pour un voyage en France</title>
        <style>
            body {
                text-align: center;
            }
        </style>
    </head>
    <body>
        <h1>Bienvenue sur notre application PyCar, le premier calculateur d'itinéraire pour un véhicule électrique prenant en compte les bornes de recharge présentes sur le territoire français</h1>
        <form method="post" action="/calcul">
            <label for="destination">Destination en France :</label>
            <input type="text" id="destination" name="destination"><br>
            <label for="depart">Point de départ :</label>
            <input type="text" id="depart" name="depart"><br>
            <label for="autonomie">Autonomie de votre véhicule électrique (en km) :</label>
            <input type="number" id="autonomie" name="autonomie"><br>
            <input type="submit" value="Calculer">
        </form>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)
