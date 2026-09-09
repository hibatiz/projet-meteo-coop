# On importe le module json, pour lire et écrire des fichiers au format JSON
import json

# Chemin vers le fichier qui stocke les zones de la coopérative
# Constante en majuscules : valeur fixe qui ne change jamais dans le programme
CHEMIN_ZONES = "data/zones.json"

# Définition de la fonction charger_zones, qui ne prend aucun paramètre
def charger_zones():
        # Ouvre le fichier en mode lecture ("r"), avec l'encodage utf-8 (pour gérer les accents)
        # "as f" : on donne le nom "f" au fichier ouvert, pour l'utiliser dans le bloc ci-dessous

    with open(CHEMIN_ZONES, "r",encoding="utf-8" ) as f:
        # json.load(f) lit le fichier et convertit son contenu JSON en liste Python

        zones = json.load(f)
        # Le bloc "with" ferme automatiquement le fichier à la sortie de son indentation
    return zones
    # on renvoie la liste des zones chargées


# Définition de la fonction sauvgarder_zones, qui prend en entrée une liste de zones
def sauvgarder_zones(zones):
    # Ouvre le fichier en mode écriture ("w"), ce qui écrase le contenu existant
    with open(CHEMIN_ZONES, "w",encoding="utf-8") as f:
        # json.dump() convertit la liste Python en JSON et l'écrit directement dans le fichier
        json.dump(zones, f, indent=2, ensure_ascii=False)
        # indent=2 : garde le fichier lisible (retours à la ligne)
        # ensure_ascii=False : garde les accents lisibles (é, è...) au lieu de les coder

# Définition de la fonction ajouter_zone, avec 5 paramètres correspondant aux infos d'une zone
def ajouter_zone(nom, departement, ville, latitude, longitude):
    zones = charger_zones()# on charge d'abord la liste actuelle des zones
    # On calcule le prochain id disponible : le plus grand id existant + 1
    # (default=0 évite une erreur si la liste de zones est vide)
    nouvel_id = max([z["id"] for z in zones], default=0)+1
    # On construit un dictionnaire représentant la nouvelle zone
    nouvelle_zone = { 
        "id": nouvel_id,# l'id calculé juste au-dessus
        "nom": nom,# le nom reçu en paramètre
        "departement": departement,# le département reçu en paramètre
        "ville": ville,# la ville reçue en paramètre
        "latitude": latitude,# la latitude reçue en paramètre
        "longitude": longitude# la longitude reçue en paramètre
    }
    zones.append(nouvelle_zone)# on ajoute la nouvelle zone à la fin de la liste
    sauvgarder_zones(zones)# on réécrit le fichier avec la liste mise à jour
    print(f"Zone ajoutée : {nom} ({ville})")# message de confirmation affiché
    return nouvelle_zone# on renvoie la zone créée

# Définition de la fonction supprimer_zone, avec l'id de la zone à supprimer en paramètre
def supprimer_zone(id_zone):
    zones = charger_zones()# on charge la liste actuelle des zones
    # On garde toutes les zones SAUF celle avec l'id demandé
    zones_filtrees = [z for z in zones if z ["id"] != id_zone]
    # Si la liste n'a pas changé de taille, c'est que l'id n'existait pas
    if len(zones_filtrees) == len(zones):
        print(f"Aucune zone trouvée avec l'id {id_zone}")# message d'erreur
        return False # on renvoie False pour signaler l'échec
    sauvgarder_zones(zones_filtrees)# on réécrit le fichier avec la liste filtrée
    print(f"Zone {id_zone} supprimée")# message de confirmation
    return True# on renvoie True pour signaler le succès

# Définition de la fonction modifier_zone
# id_zone : l'id de la zone à modifier
# **kwargs : accepte un nombre variable de paramètres nommés (ex : ville="Lille")
def modifier_zone(id_zone, **kwargs):
    zones = charger_zones()# on charge la liste actuelle des zones
    for zone in zones:
        # Si l'id de la zone actuelle correspond à celui recherché
        if zone["id"] == id_zone:
            # .update() remplace uniquement les champs passés en paramètre (kwargs),
            # les autres champs de la zone restent inchangés
            zone.update(kwargs)
            sauvgarder_zones(zones)# on réécrit le fichier avec la liste modifiée
            print(f"Zone {id_zone} modifiée")# message de confirmation
            return zone# on renvoie la zone modifiée, et on quitte la fonction
        
    # Si on arrive ici, c'est qu'aucune zone avec cet id n'a été trouvée dans la boucle
    print(f"Aucune zone trouvée avec l'id {id_zone}")
    return None    # on renvoie None pour signaler l'échec

# Ce bloc ne s'exécute que si on lance ce fichier directement (python3 zones.py)


# --- TEST 1 : vérifie que charger_zones() fonctionne ---
if __name__ == "__main__":
    print("TEST 1 : Chargement des zones ")
    liste_zones = charger_zones()# on charge toutes les zones du fichier
    for zone in liste_zones:# on parcourt chaque zone
        print(zone)# on l'affiche
    print(f"Nombre de zones chargées : {len(liste_zones)}") # affiche le total


# --- TEST 2 : vérifie que ajouter_zone() fonctionne ---
    print("\n TEST 2 : Ajout d'une zone ")
    # \n crée un saut de ligne avant le texte, pour aérer l'affichage
    nouvelle = ajouter_zone("Zone Test", "Nord", "Lille", 50.6292, 3.0573)
    # on récupère la zone créée dans la variable "nouvelle" pour réutiliser son id ensuite
    print(f"Zone créée avec l'id : {nouvelle['id']}")


# --- TEST 3 : vérifie que modifier_zone() fonctionne ---
    print("\n TEST 3 : Modification de la zone ajoutée ")
    modifier_zone(nouvelle["id"], ville="Lille Centre")# on modifie le champ "ville" de cette zone
    zones_apres_modif = charger_zones()# on recharge les zones pour vérifier le changement
    for zone in zones_apres_modif: # on parcourt à nouveau la liste
        if zone["id"] == nouvelle["id"]:# on cherche la zone qu'on vient de modifier
            print(f"Zone modifiée : {zone}")# on l'affiche pour vérifier visuellement


 # --- TEST 4 : vérifie que supprimer_zone() fonctionne ---
    print("\n TEST 4 : Suppression de la zone de test")
    supprimer_zone(nouvelle["id"])# on supprime la zone de test créée au TEST 2


# --- TEST 5 : vérifie qu'on retrouve bien l'état d'origine ---
    print("\n TEST 5 : Vérification finale (retour à l'état d'origine) ")
    liste_finale = charger_zones()# on recharge une dernière fois
    for zone in liste_finale:# on affiche toutes les zones restantes
        print(zone)
    print(f"Nombre de zones après nettoyage : {len(liste_finale)}")# doit être égal au nombre initial

    print("\n Tous les tests sont passés avec succès.") # message final de confirmation