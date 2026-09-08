import requests

# URL de base de l'API Open-Meteo (prévisions météo)
URL_BASE = "https://api.open-meteo.com/v1/forecast"

def get_meteo(latitude,longitude):
    """
    Appelle l'API Open-Meteo pour récupérer les prévisions météo d'un lieu donné.
    Retourne les données brutes de l'API (dictionnaire) ou None en cas d'erreur.
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_min,temperature_2m_max,precipitation_sum",
        "timezone": "Europe/Paris"
         }
    try:
        reponse = requests.get(URL_BASE, params=params)
        if reponse.status_code == 200:
            return reponse.json()
        else:
            print(f"Erreur API : {reponse.status_code}")
            return None
    except requests.exceptions.ConnectionError:
     # Cas où il n'y a pas de connexion internet
        print("Erreur : pas de connexion internet")
        return None
    except requests.exceptions.Timeout:
    # Cas où l'API met trop de temps à répondre
        print("Erreur : l'API met trop de temps à répondre")
        return None
    
def extraire_donnees_utiles(donnees_api):
     """
     Simplifie les données brutes de l'API en ne gardant que l'essentiel :
     la température minimale et les précipitations du jour le plus proche.
     """
     if donnees_api is None:
          return None
     # [0] = premier jour de la liste renvoyée par l'API, donc le jour le plus proche
     temp_min = donnees_api["daily"]["temperature_2m_min"][0]
     precipitations = donnees_api["daily"]["precipitation_sum"][0]

     return{
         "temp_min": temp_min,
         "precipitations": precipitations
         }
# Ce bloc ne s'exécute que si on lance ce fichier directement (python3 meteo.py)
# Il ne s'exécute PAS si Jenny importe ce fichier depuis main.py


if __name__ == "__main__":
        print("Début du script")
        resultat = get_meteo(49.8941, 2.2958)
        donnees = extraire_donnees_utiles(resultat)
        print("Données utiles :")
        print(donnees)
        print("Fin du script")