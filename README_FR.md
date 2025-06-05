
# 🧾 Système de Gestion de Commandes

> Ceci est mon tout premier projet d’envergure, réalisé à l’hiver 2024 dans le cadre de ma formation en programmation embarquée et en Python.
>
> **🧪 Il s’agit d’un projet issu de mes premiers apprentissages — bien que fonctionnel, la structure du code et la modularité peuvent être améliorées.

## 📌 Objectif

Ce projet est une extension d'un premier système de gestion de commandes, enrichi de fonctionnalités avancées telles que :

- Interface utilisateur via Pygame et Tkinter
- Gestion d'états de commandes : En attente, En traitement, Expédiée
- Journalisation dans des fichiers CSV et JSON
- Envoi d'emails automatiques pour certaines actions
- Authentification par code PIN pour valider une commande
- Affichage de l'heure et de la température actuelle via l'API OpenWeatherMap
- Support physique : boutons, LEDs, buzzer avec gestion GPIO sur Raspberry Pi
- Début de l'apprentissage de l'architecture modulaire en Python

## 🗂️ Structure du projet

📁 Fichiers_json_csv_log/          ← Contient les logs et fichiers de commandes  
📁 Gestionnaire de commandes/      ← Code source principal, organisé en modules  
📄 config.yaml                     ← Fichier YAML de configuration (GPIO, API)  
📄 Diagramme_etat.pdf              ← Diagramme d’état des commandes  
📄 schema_de_montage.pdf           ← Schéma de montage des composants GPIO  
🖼️ icon_*.png                      ← Icônes utilisées dans l'interface  

### 📁 Modules principaux

- `main.py` : point d’entrée principal de l’application
- `gpio_manager.py` : gestion des entrées/sorties physiques (boutons, LEDs, buzzer)
- `tkinter_manager.py` : clavier numérique, interface de confirmation
- `pillow_manager.py` : affichage des images via PIL
- `email_manager.py` : envoi d’email via SMTP
- `weather_manager.py` : récupération de la température via OpenWeatherMap
- `logger_manager.py` : gestion des logs
- `status.py` : logique des statuts
- `table_manager.py` : lecture/écriture des fichiers de commande
- `config_loader.py` : chargement des données YAML
- `utils.py` : fonctions utilitaires

## 📦 Dépendances

yaml  
smtplib  
time  
RPi.GPIO  
gpiozero  
json  
os  
uuid  
logging  
pygame  
sys  
threading  
csv  
PIL  
enum  
tkinter  
requests  
io  

### Installation des dépendances :

```bash
pip install pyyaml pygame pillow requests gpiozero
sudo apt install python3-tk
```

⚠️ RPi.GPIO est spécifique à Raspberry Pi. Si vous développez sous Windows, utilisez des mocks pour éviter les erreurs GPIO.

## 🚀 Lancement

```bash
python Gestionnaire\ de\ commandes/main.py
```

## 🔐 Sécurité

- Le passage d'une commande au statut Expédiée nécessite un code PIN.
- La configuration (GPIO, clé API météo) est gérée via un fichier YAML.

## 👩‍💻 Auteurs

Projet réalisé par :    
- Nadia Simard Villa, étudiante en AEC Internet des objets et intelligence artificielle
- Sophie Mercier, étudiante en AEC Internet des objets et intelligence artificielle
    
    Sous la supervision de Khalil Loghlam, enseignant, ing. en Génie électrique et logiciel
