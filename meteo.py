import requests
URL_BASE = "https://api.open-meteo.com/v1/forecast"

def get_meteo(latitude,longitude):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_min,temperature_2m_max,precipitation_sum",
        "timezone": "Europe/Paris"
         }
    reponse = requests.get(URL_BASE, params=params)
    if reponse.status_code == 200:
        return reponse.json()
    else:
        print(f"Erreur API : {reponse.status_code}")
        return None
    
def extraire_donnees_utiles(donnees_api):
     if donnees_api is None:
          return None
     temp_min = donnees_api["daily"]["temperature_2m_min"][0]
     precipitations = donnees_api["daily"]["precipitation_sum"][0]

     return{
         "temp_min": temp_min,
         "precipitations": precipitations
         }

def get_meteo(latitude, longitude):
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
          print("Erreur : pas de connexion internet")
          return None
     except requests.exceptions.Timeout:
          print("Erreur : l'API met trop de temps à répondre")
          return None

if __name__ == "__main__":
        print("Début du script")
        resultat = get_meteo(49.8941, 2.2958)
        donnees = extraire_donnees_utiles(resultat)
        print("Données utiles :")
        print(donnees)
        print("Fin du script")