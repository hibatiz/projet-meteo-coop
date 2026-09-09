"""
risque.py - logique de détection des risques climatiques

Ce module prend en entrée les prévisions météo d'une zone (meteo.py) et détermine si des risques météorologiques existe,
selon des seuils configurables

Format attendu en entrée (dict retourné par meteo.get_meteo, ou None si l'appel API a échoué) :
{
    "daily": {
        "time": ["2026-09-09", "2026-09-10", ...],
        "temperature_2m_min": [-1.5, 2.0, ...],
        "temperature_2m_max": [8.0, 10.0, ...],
        "precipitation_sum": [0.0, 0.0, ...],
    }
}
"""

# --- Seuils ---
SEUIL_GEL_C = 0.0               # température min pour risque de gel
SEUIL_SECHERESSE_JOURS = 7      # nb de jours sans pluie
SEUIL_PLUIE_MM = 1.0            # en dessous de ce cumul, pas de pluie

def detecter_risque_gel(previsions: dict) -> list[dict]:
    """
    Parcours les prévisions journalières et retourne la liste des jours à risque de gel

        ENTRÉE :
        previsions (dict | None) - format Open-Meteo, doit contenir au minimum :
            {
                "daily": {
                    "time": ["2026-09-09", "2026-09-10", ...],
                    "temperature_2m_min": [-1.5, 2.0, ...],
                }
            }
            Peut être None si l'appel API a échoué (voir meteo.get_meteo).

    SORTIE :
        list[dict] - un dict par jour à risque, ex :
            [{"date": "2026-09-09", "temp_min": -1.5}, ...]
        Retourne une liste vide [] si aucun jour à risque, ou si previsions est None.
    """
    if previsions is None:
        return []

    daily = previsions.get("daily", {})
    dates = daily.get("time", [])
    temps_min = daily.get("temperature_2m_min", [])

    risques = []
    for date, temp_min in zip(dates, temps_min):
        if temp_min is not None and temp_min <= SEUIL_GEL_C:
            risques.append({"date": date, "temp_min": temp_min})
    return risques

def detecter_risque_secheresse(previsions: dict) -> dict | None :
    """
    Vérifie s'il existe une séquence de SEUIL_SECHERESSE_JOURS jours consécutifs sans pluie

        ENTRÉE :
        previsions (dict | None) - format Open-Meteo, doit contenir au minimum :
            {
                "daily": {
                    "time": ["2026-09-09", "2026-09-10", ...],
                    "precipitation_sum": [0.0, 0.0, ...],
                }
            }
            Peut être None si l'appel API a échoué (voir meteo.get_meteo).

    SORTIE :
        dict | None - décrit la première séquence sèche trouvée, ex :
            {"debut": "2026-09-09", "fin": "2026-09-15", "nb_jours": 7}
        Retourne None si aucune séquence de SEUIL_SECHERESSE_JOURS jours
        consécutifs sans pluie n'est trouvée, ou si previsions est None.
    """
    if previsions is None:
        return None

    daily = previsions.get("daily", {})
    dates = daily.get("time", [])
    precipitations = daily.get("precipitation_sum", [])

    jours_secs_consecutifs = 0 
    debut_sequence = None

    for date, pluie in zip(dates, precipitations):
        pluie = pluie or 0.0
        if pluie < SEUIL_PLUIE_MM:
            if jours_secs_consecutifs == 0:
                debut_sequence = date
            jours_secs_consecutifs += 1
            if jours_secs_consecutifs >= SEUIL_SECHERESSE_JOURS:
                return {
                    "debut": debut_sequence,
                    "fin": date,
                    "nb_jours": jours_secs_consecutifs,
                }
        else:
            jours_secs_consecutifs = 0
            debut_sequence = None

    return None

def analyser_zone(nom_zone: str, previsions: dict) -> dict:
    """
    Analayse complète d'une zone : combine gel + sécheresse.
    C'est cette fonction que Main.py apellera.

        ENTRÉE :
        nom_zone (str) - nom de la zone/ville, ex : "Auch"
        previsions (dict | None) - format Open-Meteo (voir detecter_risque_gel
            et detecter_risque_secheresse pour le détail des champs requis)
            Peut être None si l'appel API a échoué (voir meteo.get_meteo).

    SORTIE :
        dict - prêt à être ajouté au rapport final, ex :
            {
                "zone": "Auch",
                "risque_gel": [{"date": "2026-09-09", "temp_min": -1.5}, ...],
                "risque_secheresse": {"debut": ..., "fin": ..., "nb_jours": ...} ou None,
                "alerte": True/False,  # True si gel OU sécheresse détecté
                "erreur": True/False,  # True si previsions était None (échec API)
            }
    """
    erreur = previsions is None
    risque_gel = detecter_risque_gel(previsions)
    risque_secheresse = detecter_risque_secheresse(previsions)

    return {
        "zone": nom_zone,
        "risque_gel": risque_gel,
        "risque_secheresse": risque_secheresse,
        "alerte": bool(risque_gel) or risque_secheresse is not None,
        "erreur": erreur,
    }