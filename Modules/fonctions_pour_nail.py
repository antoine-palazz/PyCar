

def cout_distance_thermique(dist, prix_essence, essence = True):
    """ 
    Parameters:
    -----------
    dist : une distance (en kilomètres)
    prix_essence : prix de l'essence à une date t (exemple : 1.8€/l)
    essence : True par défaut (si False, signifie que c'est un véhicule Diesel)
    -----------
    N.B : 
    En 2021, une voiture particulière essence consommait en moyenne 7,54 litres pour parcourir 100 kilomètres 
    contre 6,11 pour les voitures diesel.
    -----------
    return : 
    -----------
    coût pour parcourir la distance 
    """
    if essence == True: 
        conso_100k = 7.54  #nombre de litre consommé par le véhicule à essence sur 100km  
        
    else: 
        conso_100k = 6.11  #nombre de litre consommé par le véhicule disesel sur 100km 
    
    nb_litre_trajet = (dist * conso_100k) / 100  #nombre de litre consommé par le véhicule sur la distance dist 
    cout_trajet = nb_litre_trajet * prix_essence  #coût du trajet 
    return cout_trajet 

def distance_entre_2_bornes(borne1, borne2):
    """ 
    Parameters:
    -----------
    borne1 : [lat1, lon1] 
    borne2 : [lat2, lon2]
    -----------
    return : 
    -----------
    retourne le nombre de km à parcourir pour aller de la borne 1 à la borne 2 
    """
    # Naïl je te laisse faire, c'est toi l'expert 
    return None


def cout_trajet_electrique(start, autonomie_véhicule, autonomie_start, dist, liste_localisation_bornes, prix):
    """ 
    Parameters:
    -----------
    start : [lat, lon] point de départ du véhicule électrique
    autonomie_véhicule : autonomie du véhicule si rechargé à 100% (exemple : 500km)
    autonomie_start : autonomie du véhicule au départ (exemple : 200km)
    dist : distance que le véhicule souhaite parcourir
    liste_localisation_bornes : liste contenant la localisation des bornes et le prix du kWH sur lesquelles le véhicule va s'arrêter
    pour se recharger (chaque élément de la liste est un triplet du type : [lat, lon, prix])
    conso : conso du véhicule (exemple : 17 kWh/100 km)
    prix : prix du kWh (exemple : 0.50€)
    -----------
    N.B : 
    Un véhicule électrique consomme entre 15 et 18 kWh pour effectuer 100 km en milieu urbain et extra-urbain. 
    Et consomme 20 à 25 kWh pour 100 km parcourus sur autoroute.
    -----------
    Return : 
    -----------
    coût pour qu'à la fin du voyage, le véhicule soit rechargé à 100% 
    """
    cout_total = 0
    for i, sous_liste in enumerate(liste_localisation_bornes): 
        prix_borne = sous_liste[2]
        if i==0:
            distance = distance_entre_2_bornes(start, sous_liste[0:2])  #distance entre le point de départ et la borne 1
        else: # i > 0
            sous_liste_avant = liste_localisation_bornes[i-1]
            borne_avant = sous_liste_avant[0:2]  #[lat, lon]
            distance = distance_entre_2_bornes(borne_avant, sous_liste[0:2])  #distance entre la borne i-1 et i
        autonomie_restante = autonomie_start - distance
        if autonomie_restante<=0:
            print(f"Le trajet trouvé n'est pas le bon, le véhicule tombe en panne avant d'avoir pu atteindre la borne {i}")
        else: 
            nb_km_remplir = autonomie_véhicule - autonomie_restante  #nb de km qu'il faut pour que le véhicule ait une autonomie max
            prix_100km = 20 * prix  #on suppose que le véhicule roule sur une autoroute (donc 20kwH pour 100km)
            cout_auto_max = (nb_km_remplir * prix_100km) / 100  #prix pour que le véhicule soit à son autonomie maximale
            cout_total += cout_auto_max  #actualisation du coût total
    return cout_total