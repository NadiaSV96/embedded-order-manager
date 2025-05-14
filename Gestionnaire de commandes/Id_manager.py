import json
import os
import uuid

def generate_unique_id():
    existing_ids = set()

    # Lire les IDs existants dans le fichier JSON
    if os.path.exists("commandes.json"):
        with open("commandes.json", mode="r") as file:
            data_table = json.load(file)
            print("Donnees chargees depuis le fichier JSON:", data_table)  # Affiche les données pour déboguer
            for row in data_table:
                # Verifiez ici la structure de 'row'
                if isinstance(row, dict):  # S'assurer que 'row' est un dictionnaire
                    existing_ids.add(row.get("ID"))  # Utiliser la méthode `get` pour éviter des erreurs si "ID" n'existe pas
               

    while True:
        new_id = str(int(uuid.uuid4().int % 1e6)) 
        if new_id not in existing_ids:  
            return new_id