# table_manager.py
import pygame
from config_loader import CONFIG
from status import status  


# Initialisation de Pygame
pygame.init()

# Paramètres de la table
table_start_x = CONFIG["ui"]["table_start_x"]
table_start_y = CONFIG["ui"]["table_start_y"]
table_width = CONFIG["ui"]["table_width"]
font = pygame.font.Font(None, CONFIG["ui"]["font_size"])

def draw_table(screen, data_table):
    # Dessiner le contour gris de la table
    pygame.draw.rect(screen, CONFIG["colors"]["grey"], (table_start_x, table_start_y - 20, table_width, len(data_table) * 30 + 30), 2)

    # Dessiner le fond gris de l'en-tête
    pygame.draw.rect(screen, CONFIG["colors"]["grey"], (table_start_x, table_start_y - 20, table_width, 30))

    # Dessiner les en-têtes
    headers = ['ID', 'Prix', 'Description', 'Date', 'Statut', 'Image']
    for i, header in enumerate(headers):
        headers_text = font.render(header, True, CONFIG["colors"]["black"])
        screen.blit(headers_text, (table_start_x + i * 150, table_start_y - 10))

    # Dessiner les lignes de commande
    for i, row in enumerate(data_table):
        for j, cell in enumerate(row[:-1]):  # On n'inclut pas la colonne du statut ici
            # Convertir chaque cellule en chaîne de caractères
            cell_text = str(cell)
            text = font.render(cell_text, True, CONFIG["colors"]["black"])
            screen.blit(text, (table_start_x + j * 150, table_start_y + i * 30 + 12))

        # Affichage du statut
        status_text = row[4]  # La colonne 'Statut'
        
        # Vérification de la validité du statut avant de l'utiliser
        if status_text == "En attente":
            status_command = status.ATTENTE
        elif status_text == "En traitement":
            status_command = status.TRAITEMENT
        elif status_text == "Expédiée":
            status_command = status.EXPEDIEE
        else:
            # Si le statut est inconnu, on peut afficher "Inconnu"
            status_command = status.INCONNU  # Assurez-vous d'avoir ce statut dans votre classe `status`

        # Assurez-vous que `status_command.label` est une chaîne de caractères
        status_label_text = str(status_command.label)  # Convertir en chaîne
        status_text_render = font.render(status_label_text, True, CONFIG["colors"]["black"])
        screen.blit(status_text_render, (table_start_x + 4 * 150 + 4, table_start_y + i * 30 + 12))

        # Affichage du cercle de statut
        circle_x = table_start_x + 4 * 105 + 150 + 20
        circle_y = table_start_y + i * 30 + 20
        status_command.draw_status_circle(screen, circle_x, circle_y)

class DropdownMenu:
    def __init__(self, x, y, width, height, options, title="Menu"):
        self.rect = pygame.Rect(x, y, width, height)
        self.options = options
        self.dropdown_open = False
        self.selected = None
        self.option_rects = []
        self.height = height
        self.option_height = 35
        self.title = title
        
    def draw(self, screen):
        # Dessiner le titre
        font = pygame.font.Font(None, CONFIG["ui"]["font_size"])
        title_text = font.render(self.title, True, CONFIG["colors"]["black"])
        screen.blit(title_text, (self.rect.x, self.rect.y - 20))  # Afficher le titre au-dessus du menu

        # Dessiner le rectangle du menu
        pygame.draw.rect(screen, CONFIG["colors"]["white"], self.rect)
        pygame.draw.rect(screen, CONFIG["colors"]["black"], self.rect, 2)
        
        # Afficher le texte du bouton
        text = font.render(self.selected if self.selected else "Choisissez une option", True, CONFIG["colors"]["black"])
        screen.blit(text, (self.rect.x + 10, self.rect.y + 10))
        
        # Si le menu déroulant est ouvert, afficher les options
        if self.dropdown_open:
            self.option_rects = []  # Réinitialiser les rectangles d'option à chaque ouverture
            for idx, option in enumerate(self.options):
                option_rect = pygame.Rect(self.rect.x, self.rect.y + self.height + idx * self.option_height, self.rect.width, self.option_height)
                pygame.draw.rect(screen, CONFIG["colors"]["white"], option_rect)
                pygame.draw.rect(screen, CONFIG["colors"]["black"], option_rect, 2)
                option_text = font.render(option, True, CONFIG["colors"]["black"])
                screen.blit(option_text, (option_rect.x + 10, option_rect.y + 10))
                self.option_rects.append(option_rect)
                
    def toggle(self):
        self.dropdown_open = not self.dropdown_open
        
    def select(self, pos):
        for idx, option_rect in enumerate(self.option_rects):
            if option_rect.collidepoint(pos):
                self.selected = self.options[idx]
                self.dropdown_open = False
                return True
        return False
    
    def reset(self):
        """Réinitialiser la sélection à l'option par défaut."""
        self.selected = None
        print("Menu réinitialisé")  # Pour vérifier si la fonction est bien appelée
    

descriptions = []

# Classe pour gérer les commandes
class Description:
    def __init__(self, description):
        self.description = description
    
    def draw(self, screen, y_offset):
        # Dessiner la ligne de commande (tableau)
        pygame.draw.rect(screen,  CONFIG["colors"]["grey"], pygame.Rect(50, y_offset, 600, 40))  # Fond gris de la ligne
        pygame.draw.rect(screen,  CONFIG["colors"]["black"], pygame.Rect(50, y_offset, 600, 40), 2)  # Bordure de la ligne

        # Afficher la description de la commande
        description_text = CONFIG["ui"]["font_size"].render(self.description, True,  CONFIG["colors"]["black"])
        screen.blit(description_text, (60, y_offset + 10))  # Décalage pour l'alignement
        

def add_commande(dropdown_menu):
    if dropdown_menu.selected:  # Vérifier si une option a été choisie dans le menu déroulant
        description_text = dropdown_menu.selected  # Utiliser l'option sélectionnée
    else:
        description_text = "Aucune"  # Si aucune option n'est choisie, mettre une valeur par défaut

    dropdown_menu.reset()
    
       
    # Ajouter la description à la commande
    descriptions.append(Description(description_text))  # Créer la commande avec la description choisie

    

    