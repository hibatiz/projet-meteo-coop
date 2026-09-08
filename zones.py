import json

# Chemin vers le fichier qui stocke les zones de la coopérative
CHEMIN_ZONES = "data/zones.json"

def charger_zones():
    with open(CHEMIN_ZONES, "r",encoding="utf-8" ) as f:
        zones = json.load(f)
    return zones

def sauvgarder_zones(zones):
    with open(CHEMIN_ZONES, "w",encoding="utf-8") as f:
        json.dump(zones, f, indent=2, ensure_ascii=False)
        # indent=2 : garde le fichier lisible (retours à la ligne)
        # ensure_ascii=False : garde les accents lisibles (é, è...) au lieu de les coder

def ajouter_zone(nom, departement, ville, latitude, longitude):
    zones = charger_zones()
    # On calcule le prochain id disponible : le plus grand id existant + 1
    # (default=0 évite une erreur si la liste de zones est vide)
    nouvel_id = max([z["id"] for z in zones], default=0)+1
    nouvelle_zone = { 
        "id": nouvel_id,
        "nom": nom,
        "departement": departement,
        "ville": ville,
        "latitude": latitude,
        "longitude": longitude
    }
    zones.append(nouvelle_zone)
    sauvgarder_zones(zones)
    print(f"Zone ajoutée : {nom} ({ville})")
    return nouvelle_zone

def supprimer_zone(id_zone):
    zones = charger_zones()
    # On garde toutes les zones SAUF celle avec l'id demandé
    zones_filtrees = [z for z in zones if z ["id"] != id_zone]
    # Si la liste n'a pas changé de taille, c'est que l'id n'existait pas
    if len(zones_filtrees) == len(zones):
        print(f"Aucune zone trouvée avec l'id {id_zone}")
        return False
    sauvgarder_zones(zones_filtrees)
    print(f"Zone {id_zone} supprimée")
    return True
def modifier_zone(id_zone, **kwargs):
    zones = charger_zones()
    for zone in zones:
        if zone["id"] == id_zone:
            # .update() remplace uniquement les champs passés en paramètre (kwargs),
            # les autres champs de la zone restent inchangés
            zone.update(kwargs)
            sauvgarder_zones(zones)
            print(f"Zone {id_zone} modifiée")
            return zone
    print(f"Aucune zone trouvée avec l'id {id_zone}")
    return None    

# Ce bloc ne s'exécute que si on lance ce fichier directement (python3 zones.py)
# Il ne s'exécute PAS si Jenny importe ce fichier depuis main.py

if __name__ == "__main__":
    print("Chargement des zones...")
    liste_zones = charger_zones()
    for zone in liste_zones:
        print(zone)
    print(f"\nNombre de zones chargées : {len(liste_zones)}")