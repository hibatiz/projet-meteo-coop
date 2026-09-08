"""
risque.py - logique de détection des risques climatiques

Ce module prend en entrée les prévisions météo d'une zone (meteo.py) et détermine si des risques météorologiques existe,
selon des seuils configurables
"""

# --- Seuils ---
SEUIL_GEL_C = 0.0               # température min pour risque de gel
SEUIL_SECHERESSE_JOURS = 7      # nb de jours sans pluie
SEUIL_PLUIE_MM = 1.0            # en dessous de ce cumul, pas de pluie

def detecter_risque_gel(previsions: dict) -> list[dict]:
    """
    Parcours les prévisions journalières et retourne la liste des jours à risque de gel
    """
    daily = previsions.get("daily", {})
    dates = daily.get("time", [])
    temps_min = daily.get ("temperature_2m_min", [])

    risques = []
    for date, temp_min in zip(dates, temps_min):
        if temp_min is not None and temp_min < SEUIL_GEL_C:
            risques.append({"date": date, "temp_min": temp_min})
    return risques

def detecter_risque_secheresse(previsions: dict) -> dict | None :
    """
    Vérifie s'il existe une séquence de SEUIL_SECHERESSE_JOURS jours consécutifs sans pluie
    """
    daily = previsions.get("daily", {})
    dates = daily.get("time", [])
    precipitations = daily.get ("pricipation_sum", [])

    jours_secs_consecutifs = 0 
    debut_sequence = None

    for date, pluie in zip (dates, precipitations):
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
    """
    risque_gel = detecter_risque_gel(previsions)
    risque_secheresse = detecter_risque_secheresse(previsions)

    return {
        "zone": nom_zone,
        "risque_gel": risque_gel,
        "risque_secheresse": risque_secheresse,
        "alerte": bool(risque_gel) or risque_secheresse is not None,
    }