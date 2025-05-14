import pygame
import sys
import threading
from config_loader import CONFIG
from email_manager import send_email  
from table_manager import draw_table, DropdownMenu, add_commande, descriptions, Description
from text_edit import text_edit
from status import status
from utils import get_current_date, get_current_time
from gpio_manager import setup_gpio, allumer_led, eteindre_led, arreter_buzzer, clignoter_led, sonner_buzzer, nettoyer_gpio
from logger_manager import get_logger
from Id_manager import generate_unique_id
from tkinter_manager import demander_pin, demander_confirmation_fermeture
from weather_manager import get_weather
from pillow_manager import draw_icons
import json
import time
import RPi.GPIO as GPIO
import csv


pygame.init()

# Paramètres de l'écran
screen_width = CONFIG["screen"]["width"]
screen_height = CONFIG["screen"]["height"]
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Gestionnaire de commandes")

# Paramètre du tableau de commandes
table_start_x = CONFIG["ui"]["table_start_x"]
table_start_y = CONFIG["ui"]["table_start_y"]

# Paramètre d'affichage pour temperature et de controle
temperature_x = screen_width - 230
temperature_y = 15

icon_rect = pygame.Rect(screen_width-50, 0, 50, 50)

last_weather_update = 0  # Temps de la derniere mise a jour
weather_update_interval = 600  # Intervalle en secondes (par exemple, 10 minutes)

# Dimensions du bouton "Ajouter"
button_width = 100
button_height = 40
button_rect = pygame.Rect(screen_width - 230, 265, button_width, button_height)

# Titre à afficher à droite de l'image 
title_text = "Gestionnaire de commandes"  # Le texte du titre
title_surface = pygame.font.Font(None, CONFIG["ui"]["font_size"]).render(title_text, True, CONFIG["colors"]["black"])

# Charger l'image
try:
    img = pygame.image.load('gap-logo-png-transparent.png')  # Assurez-vous que le fichier est dans le bon répertoire
    img = pygame.transform.rotozoom(img, 0, 0.07)  # Redimensionner l'image si nécessaire
    rect = img.get_rect()
    rect.topleft = (0, 0)  # Positionner l'image en haut à gauche
except pygame.error as e:
    print(f"Erreur de chargement de l'image: {e}")
    img = None  # Si l'image ne peut pas être chargée, mettre img à None  # Option de fallback

# Liste pour stocker les commandes et autres variables
commands = []
data_table = []
error_message = ""

# Nombre maximum de commandes
MAX_COMMANDES = CONFIG["max_commands"]
erreur_en_cours = False
clignotement_thread = None
clignotement_event = threading.Event()  # Créer un événement pour controler le clignotement
buzzer_thread = None

# Récupérer le logger
logger = get_logger()

# Initialisation des GPIO (LED, buzzer, bouton)
BUZZER, LED_PIN_ROUGE, QUIT_BUTTON, LED_PIN_JAUNE, LED_PIN_VERTE, EXPORT_BUTTON  = setup_gpio()


def gerer_led_par_statut(status_command, led_pin_rouge, led_pin_jaune, led_pin_verte):
    print(f"Statut de la commande: {status_command}")  # Pour déboguer et vérifier quel statut est traité

    if status_command == status.ATTENTE.label:  # Si la commande est en attente
        print("Statut: ATTENTE")
        allumer_led(led_pin_rouge)
        eteindre_led(led_pin_jaune)
        eteindre_led(led_pin_verte)
    elif status_command == status.TRAITEMENT.label:  # Si la commande est en traitement
        print("Statut: TRAITEMENT")
        eteindre_led(led_pin_rouge)
        allumer_led(led_pin_jaune)
        eteindre_led(led_pin_verte)
    elif status_command == status.EXPEDIEE.label:  # Si la commande est expédiée
        print("Statut: EXPEDIEE")
        eteindre_led(led_pin_rouge)
        eteindre_led(led_pin_jaune)
        allumer_led(led_pin_verte)
    else:
        print("Statut inconnu")

def export_data_to_csv():
    # Définir le nom du fichier CSV
    filename = "commandes_exportees.csv"
    
    # Ouvrir un fichier CSV en mode écriture
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Ajouter l'en-tête (les titres des colonnes)
        writer.writerow(["ID", "Commande", "Prix", "Date", "Statut", "Description"])
        
        # Ajouter chaque ligne de data_table
        for row in data_table:
            writer.writerow(row)
    
    logger.info(f"Les données ont été exportées vers {filename}.")
    print(f"Les données ont été exportées vers {filename}.")


#Creation d'un fichier json
def save_to_json():
    simplified_data = [row[:5] for row in data_table]
    
    with open("commandes.json", mode='w') as file:
        json.dump(simplified_data, file, indent=4)  # ecrit les donnees sous forme JSON, avec une indentation pour la lisibilité

# Sauvegarder dans le fichier JSON apres chaque ajout
save_to_json()       

def load_from_json():
    global data_table
    try:
        with open("commandes.json", mode='r') as file:
            data_table = json.load(file)  # Charge les donnees du fichier JSON
    except FileNotFoundError:
        data_table = []  # Si le fichier n'existe pas, commencer avec une table vide

# Charger les commandes depuis le JSON au démarrage
load_from_json()

# Options du menu
options = ["Chandail", "Pantalon", "Jupe", "Robe"]

# Création du menu déroulant avec un titre
dropdown_menu = DropdownMenu(400, 270, 250, 30, options, title="Description")

# Fonction pour gérer l'erreur et l'état du bouton et de la LED
def gerer_erreur():
    global erreur_en_cours, clignotement_thread, buzzer_thread, clignotement_event  
    commands_number = len(data_table)

    # Si le nombre de commandes atteint exactement 10
    if commands_number == MAX_COMMANDES :
        if data_table[-1][4] != status.EXPEDIEE.label:
            print(commands_number)
            if not erreur_en_cours:
                erreur_en_cours = True
                clignotement_event.clear() #reinitie l'event pour demarrer le clignotement 
                clignotement_thread = threading.Thread(target=clignoter_led, args=(LED_PIN_ROUGE, clignotement_event))
                clignotement_thread.start()
                logger.warning('Plus de 10 commandes. Vous ne pouvez plus ajouter de commandes')
                send_email()
                buzzer_thread = threading.Thread(target= sonner_buzzer, args=(BUZZER,))
                buzzer_thread.start()
        
        return False 

    # Si le nombre de commandes est inférieur à 10, on peut ajouter
    else:
        if erreur_en_cours:
            erreur_en_cours = False
            clignotement_event.set()  # Arreter le clignotement
            arreter_buzzer(BUZZER)
        return True  

# Fonction pour supprimer la 10ème commande si expédiée
def supprimer_10eme_commande():
    global error_message
    if len(data_table) >= MAX_COMMANDES:  # Verifier qu'il y a bien 10 commandes
        last_command = data_table[-1]  # Derniere commande
        statut = last_command[4]  # Statut de la derniere commande
        if statut == status.EXPEDIEE.label and button_rect.collidepoint(event.pos):  # Si la derniere commande est "expediee"
            del data_table[-1]  # Supprimer la derniere commande expediee

            logger.info("10eme commande expédiée et supprimée")
            print("10eme commande expédiee et supprimée")
            
            gerer_erreur()
            error_message = ""

            # Ajouter automatiquement la nouvelle commande apres suppression de la 10eme commande
            
            row = [command.text for command in commands]  
            # Ajouter la description dans la ligne de commande
            if dropdown_menu.selected:
                row.append(dropdown_menu.selected)  # Ajouter la description choisie
            else:
                row.append("Aucune")  # Valeur par défaut si aucune sélection

            # Ajouter un statut par défaut
            status_command = status.ATTENTE  
            row.append(status_command.label)  # Statut sous forme de texte
                        
            # Ajouter l'ID, la date et insérer la commande dans la table
            new_id = generate_unique_id()
            row.insert(0, new_id)  # Ajouter l'ID dans la première colonne
            current_date = get_current_date()  # Appeler la fonction pour obtenir la date actuelle
            row.insert(3, current_date)  # Ajouter la date dans la bonne colonne
            gerer_led_par_statut(row[4], LED_PIN_ROUGE, LED_PIN_JAUNE, LED_PIN_VERTE)   


            # Insérer la commande dans data_table
            data_table.insert(0, row)
            logger.info(f"Commande ajoutée {row[0]} et autorisée. Nombre de commandes: {len(data_table)}")
            print(f"Commande ajoutée et autorisée. Nombre de commandes: {len(data_table)}")

            # Sauvegarder dans le fichier JSON après chaque ajout
            save_to_json()

            # Vider les champs de texte après ajout
            for command in commands:
                command.text = ""
                dropdown_menu.reset()
            gerer_led_par_statut(row[4], LED_PIN_ROUGE, LED_PIN_JAUNE, LED_PIN_VERTE)
            
# Fonction pour afficher le message d'erreur
def afficher_message_erreur(message):
    error_surface = error_surface = pygame.font.Font(None, CONFIG["ui"]["font_size"]).render(message, True, CONFIG["colors"]["red"])
    # Positionner le message d'erreur sous le bouton Ajouter
    screen.blit(error_surface, (button_rect.x - 100, button_rect.y + button_rect.height + 10))

# Initialisation des champs de texte
commands.append(text_edit(100, 250, title="Prix"))

def draw_annuler_button(screen, row, index, table_start_x, table_start_y):
    if row[4] == status.ATTENTE.label:  # Vérifier si la commande est en "En attente"
        
        # Définir les dimensions et la position du bouton Annuler
        button_x = (table_start_x + 6 * 150) - 50
        button_y = table_start_y + index * 30 + 10
        button_width, button_height = 100, 28
        border_thickness = 2  

        # Dessiner le contour gris (légèrement plus grand)
        border_rect = pygame.Rect(button_x - border_thickness, button_y - border_thickness, button_width + 2 * border_thickness, button_height + 2 * border_thickness)
        pygame.draw.rect(screen, CONFIG["colors"]["grey"], border_rect)

        # Dessiner le bouton rouge
        cancel_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(screen, CONFIG["colors"]["red"], cancel_button_rect)

        # Dessiner le texte du bouton
        font = pygame.font.Font(None, CONFIG["ui"]["font_size"])
        cancel_button_text = font.render("Annuler", True, CONFIG["colors"]["white"])
        screen.blit(cancel_button_text, (cancel_button_rect.x + 15, cancel_button_rect.y + 5))  # Positionner le texte
        
        return cancel_button_rect  # Retourne le rectangle du bouton pour la gestion des clics
    return None


# Fonction pour annuler la commande
def annuler_commande(index):
    # Supprimer la commande de la liste data_table
    commande_id = data_table[index][0]
    del data_table[index]
    logger.info(f"Commande ID : {commande_id} annulée.")
    save_to_json()  # Sauvegarder les changements dans le fichier JSON
    print(f"Commande ID : {commande_id} annulée.")


# Boucle principale
running = True
while running:
    screen.fill(CONFIG["colors"]["white"])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if demander_confirmation_fermeture():  # Demander confirmation avant de quitter
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if button_rect.collidepoint(event.pos):  # Si on clique sur le bouton Ajouter
                    ajout_possible = gerer_erreur()
                    print(f"Vérification ajout possible : {ajout_possible}")
                    logger.info(f"Vérification ajout possible : {ajout_possible}")

                    if ajout_possible:  # Ajouter seulement si on n'a pas atteint la limite et valeur stockée
                        # Récupère le texte de chaque champ
                        row = [command.text for command in commands]  
                        
                        # Ajouter la description dans la ligne de commande
                        if dropdown_menu.selected:
                            row.append(dropdown_menu.selected)  # Ajouter la description choisie
                        else:
                            row.append("Aucune")  # Valeur par défaut si aucune sélection

                        # Ajouter un statut par défaut
                        status_command = status.ATTENTE  
                        row.append(status_command.label)  # Statut sous forme de texte
                        
                        # Ajouter l'ID, la date et insérer la commande dans la table
                        new_id = generate_unique_id()
                        row.insert(0, new_id)  # Ajouter l'ID dans la première colonne
                        current_date = get_current_date()  # Appeler la fonction pour obtenir la date actuelle
                        row.insert(3, current_date)  # Ajouter la date dans la bonne colonne

                        price = row[1]  # Supposons que row[1] contient le prix (tu peux adapter selon ton code)
                        if price:
                            row[1] = f"${price}"  # Ajouter le symbole $
                        
                        # Insérer la commande dans data_table
                        data_table.insert(0, row)
                        logger.info(f"Commande ajoutée et autorisée. Nombre de commandes: {len(data_table)}")
                        print(f"Commande ajoutée et autorisée. Nombre de commandes: {len(data_table)}")
                        gerer_led_par_statut(row[4], LED_PIN_ROUGE, LED_PIN_JAUNE, LED_PIN_VERTE)

                    
                        # Sauvegarder dans le fichier JSON après chaque ajout
                        save_to_json()

                        # Vider les champs de texte après ajout
                        for command in commands:
                            command.text = ""
                            dropdown_menu.reset()
                        
                    else:
                        logger.info("Ajout refusée : Limite atteinte")
                        print("Ajout refusée : Limite atteinte")
                        error_message = "Ajout refusé : Limite atteinte"
    
                # Gérer le menu déroulant
                if dropdown_menu.rect.collidepoint(event.pos):
                    dropdown_menu.toggle()  # Ouvrir ou fermer le menu

                # Sélectionner une option du menu déroulant
                if dropdown_menu.dropdown_open:
                    if dropdown_menu.select(event.pos):
                        print(f"Option sélectionnée: {dropdown_menu.selected}")

                # Gérer le changement de statut de commande
                for i, row in enumerate(data_table):
                    cancel_button_rect = draw_annuler_button(screen, row, i, table_start_x, table_start_y)
                    if cancel_button_rect and cancel_button_rect.collidepoint(event.pos):
                        # Annuler la commande si on clique sur le bouton Annuler
                        annuler_commande(i)
                        error_message = ""

                    status_rect = pygame.Rect(table_start_x + 4 * 150, table_start_y + i * 30 + 12, 150, 30)
                    if status_rect.collidepoint(event.pos):
                        # Trouver l'index du statut dans la ligne
                        current_status = row[4]
                        selected_index = i
                        if current_status == "En traitement":
                            def change_status_after_pin():
                                data_table[selected_index][4] = "Expédiée"
                                logger.info(f"Commande {data_table[selected_index][0]} changée à l'état 'Expédiée'")
                                gerer_led_par_statut(data_table[selected_index][4], LED_PIN_ROUGE, LED_PIN_JAUNE, LED_PIN_VERTE)  # Met à jour la LED
                                save_to_json()  # Sauvegarder la modification dans le fichier JSO
                            demander_pin(change_status_after_pin)
                            break
                        
                        elif  current_status == "En attente":
                            new_status = status.ATTENTE.next_status()
                            gerer_led_par_statut(row[4], LED_PIN_ROUGE, LED_PIN_JAUNE, LED_PIN_VERTE)
                            logger.info(f"Commande {data_table[selected_index][0]} changée à l'état 'En traitement'")
                        elif current_status == "Expédiée":
                            new_status = status.EXPEDIEE.next_status()

                        # Mettre à jour le statut dans la ligne de commande
                        row[4] = new_status.label  # Mettre à jour la valeur du statut
                        gerer_led_par_statut(row[4], LED_PIN_ROUGE, LED_PIN_JAUNE, LED_PIN_VERTE)

                supprimer_10eme_commande()  # Supprimer la 10ème commande si expédiée

                 
        for command in commands:
            command.handle_event(event)
    

    # Affichage des champs de texte
    for command in commands:
        command.draw(screen) 

    # Dessin de la table des commandes
    draw_table(screen, data_table)

    # Afficher les boutons Annuler pour chaque ligne en attente
    for i, row in enumerate(data_table):
        draw_annuler_button(screen, row, i, table_start_x, table_start_y)

    # Dessin du menu déroulant
    dropdown_menu.draw(screen)

    # Affichage du bouton "Ajouter", même si la limite de commandes est atteinte
    pygame.draw.rect(screen, CONFIG["colors"]["blue"], button_rect)
    add_text = pygame.font.Font(None, CONFIG["ui"]["font_size"]).render("Ajouter", True, CONFIG["colors"]["white"])
    screen.blit(add_text, (button_rect.x + 15, button_rect.y + 10))

    # Affichage du message d'erreur si nécessaire
    if error_message:
        afficher_message_erreur(error_message)

    # Affichage du titre à côté de l'image (avec un petit espacement)
    screen.blit(title_surface, (rect.right + 30, 75))

    # Affichage de l'image (si elle a été chargée correctement)
    if img:
        screen.blit(img, rect)  # Afficher l'image dans le coin supérieur gauche

    # Affichage de l'heure
    current_time = get_current_time()  # Appeler la fonction pour obtenir l'heure actuelle
    time_surface = pygame.font.Font(None, CONFIG["ui"]["font_size"]).render(f"Heure: {current_time}", True, CONFIG["colors"]["black"])
    screen.blit(time_surface, (rect.right + 30, 15))  # Positionner l'heure juste sous le titre
    current_time = time.time()

    # Récupérer la température et l'icone via le module météo uniquement si l'intervalle est écoulé
    if current_time - last_weather_update >= weather_update_interval:
        temperature, icon_surface = get_weather()
        last_weather_update = current_time  # Mettre a jour le temps de la derniere mise a jour

    # Affichage de la température 
    if temperature:
        temperature_surface = pygame.font.Font(None, CONFIG["ui"]["font_size"]).render(f"Température: {temperature}", True, CONFIG["colors"]["black"])
        screen.blit(temperature_surface, (temperature_x, temperature_y))

    # Affichage de l'icone meteo
    if icon_surface:
        screen.blit(icon_surface, icon_rect)

    # Dessiner les icônes de pillow
    draw_icons(screen, data_table, table_start_x, table_start_y)

    if GPIO.input(EXPORT_BUTTON) == GPIO.LOW:  # Bouton d'export
        export_data_to_csv()
        print('Exportation des données vers CSV...')
        time.sleep(1.0)

    if GPIO.input(QUIT_BUTTON) == GPIO.LOW:  # Bouton de fermeture
        if demander_confirmation_fermeture() :
            running = False
          

    # Actualiser l'affichage
    pygame.display.flip()

nettoyer_gpio()  # nettoyage propre des GPIO

# Quitter Pygame
pygame.quit()
sys.exit()
