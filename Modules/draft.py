    def distance_and_itinerary(self):

        self.get_coordo()

        origin = self.x_A
        destination = self.x_B
        api_key = "AIzaSyCnuH5NvjIYsQeKcsSPOF_ZilFXyJ2lB2A"

        gmaps = googlemaps.Client(key=api_key)

        directions_result = gmaps.directions(origin, destination, mode="driving")


        if directions_result:
            # extrait la distance totale du trajet
            distance = directions_result["routes"][0]["legs"][0]["distance"]["text"]

            trajet = []

            # affiche les étapes du trajet
            for step in directions_result[0]['legs'][0]['steps']:
                trajet.append(step)

            # renvoie la distance et l'ensemble des étapes du trajet
            return distance, trajet
        
        else:

            return "Erreur: Impossible de calculer la distance."
