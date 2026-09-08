"""
main.py - orchestration du projet meteo-coop

Ce script :
  1. Charge les zones de la coopérative (zones.py de Hiba)
  2. Récupère les prévisions météo pour chaque zone (meteo.py de Hiba)
  3. Analyse les risques climatiques pour chaque zone (risque.py)
  4. Génère un rapport structuré (CSV) listant les zones à risque

Fonctions réellement utilisées côté Hiba (à jour après son push) :
  - zones.charger_zones() -> list[dict]  (pas d'argument, lit data/zones.json en interne)
      chaque zone : {"id", "nom", "departement", "ville", "latitude", "longitude"}
  - meteo.get_meteo(latitude, longitude) -> dict | None
      renvoie la réponse brute Open-Meteo, ou None si l'appel API a échoué
"""

import csv
import sys

from zones import charger_zones
from meteo import get_meteo
from risque import analyser_zone

CHEMIN_SORTIE = "output/alertes.csv"

def analyser_toutes_zones() -> list[dict]:
    """
    Parcours toutes les zones de la coopérative, récupère la météo de chacune
    et l'analyse avec risque.py.

        ENTRÉE :
        aucune

    SORTIE :
        list[dict] - un résultat d'analyse par zone (voir risque.analyser_zone
            pour le détail du format de chaque dict)
    """
    zones = charger_zones()

    if not zones:
        print("Aucune zone trouvée. Vérifie data/zones.json.")
        return []

    resultats = []
    for zone in zones:
        nom = zone["nom"]
        print(f"Analyse de la zone : {nom} ({zone['ville']})...")

        previsions = get_meteo(zone["latitude"], zone["longitude"])
        resultat = analyser_zone(nom, previsions)
        resultats.append(resultat)

        if resultat["erreur"]:
            print(f"  Erreur : impossible de récupérer la météo pour {nom}")
        elif resultat["alerte"]:
            print(f"  Alerte détectée pour {nom}")
        else:
            print(f"  OK, pas de risque pour {nom}")

    return resultats

def generer_rapport(resultats: list[dict], chemin_sortie: str = CHEMIN_SORTIE) -> None:
    """
    Ecris les résultats d'analyse dans un fichier CSV, une ligne par zone.

        ENTRÉE :
        resultats (list[dict]) - sortie de analyser_toutes_zones()
        chemin_sortie (str) - chemin du fichier CSV à générer

    SORTIE :
        aucune (écrit le fichier sur le disque)
    """
    with open(chemin_sortie, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["zone", "alerte", "erreur", "risque_gel_jours", "risque_secheresse"])

        for r in resultats:
            jours_gel = "; ".join(
                f"{j['date']} ({j['temp_min']}°C)" for j in r["risque_gel"]
            )
            secheresse = ""
            if r["risque_secheresse"]:
                s = r["risque_secheresse"]
                secheresse = f"{s['debut']} -> {s['fin']} ({s['nb_jours']} jours)"

            writer.writerow([r["zone"], r["alerte"], r["erreur"], jours_gel, secheresse])

    print(f"Rapport généré : {chemin_sortie}")

def main():
    print("Chargement des zones...")
    resultats = analyser_toutes_zones()

    if not resultats:
        sys.exit(1)

    generer_rapport(resultats)

# Ce bloc ne s'exécute que si on lance ce fichier directement (python3 main.py)

if __name__ == "__main__":
    main()