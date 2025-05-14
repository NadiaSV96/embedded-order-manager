import yaml

def load_config():
    try:
        with open("config.yaml", "r") as file:
            config = yaml.safe_load(file)
            print("Configuration chargée :", config)  # Pour vérifier le chargement
            return config
    except FileNotFoundError:
        print("Erreur : Le fichier 'config.yaml' n'a pas été trouvé.")
        return {}
    except yaml.YAMLError as e:
        print(f"Erreur de syntaxe YAML : {e}")
        return {}

CONFIG = load_config()
