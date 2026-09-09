# On importe la librairie requests, qui permet d'envoyer des requêtes HTTP (appeler une API)
import requests

# URL de base de l'API Open-Meteo (prévisions météo)
# Constante en majuscules : valeur fixe qui ne change jamais dans le programme
URL_BASE = "https://api.open-meteo.com/v1/forecast"


# Définition de la fonction get_meteo, qui prend en entrée une latitude et une longitude
def get_meteo(latitude,longitude):
    """
    Appelle l'API Open-Meteo pour récupérer les prévisions météo d'un lieu donné.
    Retourne les données brutes de l'API (dictionnaire) ou None en cas d'erreur.
    """
    # Dictionnaire contenant tous les paramètres à envoyer à l'API
    params = {
        "latitude": latitude,# la latitude reçue en entrée de la fonction
        "longitude": longitude,# la longitude reçue en entrée de la fonction
        "daily": "temperature_2m_min,temperature_2m_max,precipitation_sum",# données journalières demandées
        "timezone": "Europe/Paris"# fuseau horaire pour des dates cohérentes
         }
    try:# Bloc try : on "surveille" le code ci-dessous pour intercepter une erreur sans planter le programme

        # Envoie la requête HTTP GET vers l'API, avec les paramètres construits ci-dessus
        reponse = requests.get(URL_BASE, params=params, timeout=5) 
        # Si le code de statut HTTP est 200, la requête a réussi
        if reponse.status_code == 200:
          # On convertit la réponse (JSON) en dictionnaire Python et on le renvoie

            return reponse.json()
        else:
          # Sinon, on affiche le code d'erreur reçu (ex : 400, 404, 500...)

            print(f"Erreur API : {reponse.status_code}")
            return None # on renvoie None pour signaler l'échec
   # Cas où il n'y a pas de connexion internet du tout
    except requests.exceptions.ConnectionError:
     # Cas où il n'y a pas de connexion internet
        print("Erreur : pas de connexion internet")
        return None# on renvoie None pour signaler l'échec
    # Cas où le serveur met trop de temps à répondre
    except requests.exceptions.Timeout:
    # Cas où l'API met trop de temps à répondre
        print("Erreur : l'API met trop de temps à répondre")
        return None

 # Définition de la deuxième fonction, qui prend en entrée les données brutes de l'API
def extraire_donnees_utiles(donnees_api):
     """
     Simplifie les données brutes de l'API en ne gardant que l'essentiel :
     la température minimale et les précipitations du jour le plus proche.
     """
     # Si les données reçues sont None (l'appel API a échoué), on ne peut rien extraire
     if donnees_api is None:
          return None # on renvoie None pour propager l'échec
     # On va chercher : section "daily" > "temperature_2m_min" > 1er élément [0]
     # [0] = premier jour de la liste renvoyée par l'API, donc le jour le plus proche
     temp_min = donnees_api["daily"]["temperature_2m_min"][0]
     # Même logique pour récupérer les précipitations du jour le plus proche
     precipitations = donnees_api["daily"]["precipitation_sum"][0]
     # On construit et renvoie un nouveau dictionnaire simplifié avec les 2 infos utiles

     return{
         "temp_min": temp_min,# la température minimale extraite
         "precipitations": precipitations# les précipitations extraites
         }
# Ce bloc ne s'exécute que si on lance ce fichier directement (python3 meteo.py)
# Il ne s'exécute PAS si Jenny importe ce fichier depuis main.py

# --- TEST 1 : appel normal avec une zone valide (Amiens) ---
if __name__ == "__main__":
    print("TEST 1 : Appel normal (Amiens) ")
    resultat = get_meteo(49.8941, 2.2958)# on appelle l'API avec les coordonnées d'Amiens
    donnees = extraire_donnees_utiles(resultat)# on simplifie le résultat
    print("Données utiles :", donnees)# on affiche le résultat simplifié


    # --- TEST 2 : appel normal avec une autre zone (Marseille) ---

    print("\nTEST 2 : Appel avec une autre zone (Marseille) ")
    # \n crée un saut de ligne avant le texte, pour aérer l'affichage
    resultat2 = get_meteo(43.2965, 5.3698)# on appelle l'API avec les coordonnées de Marseille
    donnees2 = extraire_donnees_utiles(resultat2)# on simplifie le résultat
    print("Données utiles :", donnees2)# on affiche le résultat simplifié

# --- TEST 3 : appel avec des coordonnées invalides, pour tester la robustesse ---
    print("\nTEST 3 : Coordonnées invalides (hors limites) ")
    resultat3 = get_meteo(999, 999)# 999 n'est pas une coordonnée GPS valide
    donnees3 = extraire_donnees_utiles(resultat3)# on essaie quand même de simplifier (doit gérer l'erreur)
    print("Résultat avec coordonnées invalides :", donnees3)# doit afficher None si l'erreur est bien gérée


# --- TEST 4 : vérifier que extraire_donnees_utiles gère bien un None en entrée ---
    print("\nTEST 4 : Cas où l'API renvoie None ")
    donnees4 = extraire_donnees_utiles(None)# on simule un échec de get_meteo() en passant None directement
    print("extraire_donnees_utiles(None) donne :", donnees4)# doit afficher None sans planter

    print("\nTests terminés.")# message final