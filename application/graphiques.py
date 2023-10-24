import pandas as pd
from datetime import datetime 
import os 
import plotly.express as px
import matplotlib.pyplot as plt
from io import BytesIO
import base64

os.chdir("/Users/augustincablant/Documents/GitHub/PyCar")
def evolution_nbre_voiture_elec():
    df = pd.read_csv('DOWNLOAD/Voitures.csv', sep=';')
    List_date = []
    List_nombre = []

    for row in df.itertuples():
        date0 = row.date_arrete
        date = datetime.strptime(date0, "%d/%m/%Y").strftime("%Y-%m-%d")
        nbre = row.nb_vp_rechargeables_el
        if date in List_date:
            for i in range(len(List_date)):
                if List_date[i] == date:
                    List_nombre[i] += nbre
        else:
            List_date.append(date)
            List_nombre.append(nbre)

    dict = {'Date': List_date, 'Nombre': List_nombre}

    dataframe = pd.DataFrame(dict)
    return dataframe.sort_values('Date') 
