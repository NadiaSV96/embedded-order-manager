# logger_manager.py
import logging

# Configuration des paramètres de journalisation
LOG_LEVEL = logging.DEBUG
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_FILE = "gestionnaire_de_commandes.log"

# Configuration de la journalisation
logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE),  # Journalisation dans un fichier
        logging.StreamHandler()          # Journalisation dans la console
    ]
)

# Création du logger
logger = logging.getLogger('Gestionnaire de Commandes')

# Fonction pour obtenir le logger, pour utilisation dans d'autres modules
def get_logger():
    return logger
