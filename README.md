# Projet Météo Coopérative

Détection de risques climatiques (gel, sécheresse) pour une coopérative agricole, à partir des prévisions météo par zone.

## Fonctionnement

Le programme lit une liste de zones (départements/villes françaises), interroge l'API Open-Meteo pour chacune, détecte les risques de gel et de sécheresse, et génère un fichier récapitulatif des alertes.

## Installation

```bash
pip3 install requests
```

## Lancement

```bash
python3 main.py
```

## Structure du projet

- `meteo.py` : appel à l'API Open-Meteo
- `zones.py` : gestion des zones (lecture/ajout/suppression/modification)
- `risque.py` : détection des risques (gel/sécheresse)
- `main.py` : orchestration du programme
- `data/zones.json` : données des zones de la coopérative