from PIL import Image
import pygame

# Fonction pour charger une image avec Pillow et la convertir en format compatible Pygame
def load_icon_image_pillow(image_path, size=(26,26)):
    pil_image = Image.open(image_path)  # Ouvre l'image avec Pillow
    pil_image = pil_image.convert("RGBA")  # Conversion pour garder la transparence 
    pil_image = pil_image.resize(size)  # Redimensionne l'image avec Pillow
    # Convertir l'image Pillow en une surface Pygame et la retourner
    return pygame.image.fromstring(pil_image.tobytes(), pil_image.size, pil_image.mode)

# Dictionnaire des images pour chaque vêtement
image_map = {
    "Pantalon": load_icon_image_pillow('icon_pants.png'),
    "Chandail": load_icon_image_pillow('icon_shirt.png'),
    "Jupe": load_icon_image_pillow('icon_skirt.png'),
    "Robe": load_icon_image_pillow('icon_dress.png'),
}

# Fonction pour dessiner l'icône selon la description choisie
def draw_icons(screen, data_table, table_start_x, table_start_y, icon_x_offset=15, icon_y_offset=10):
    
    for i, row in enumerate(data_table):
        description = row[2]  # Description dans la troisième colonne

        # Vérifier la description et charger l'icône correspondante
        if description in image_map:
            icon = image_map[description]

            icon_x = table_start_x + 5 * 150 + icon_x_offset
            icon_y = table_start_y + i * 30 + icon_y_offset 

            # Afficher l'icône redimensionnée
            screen.blit(icon, (icon_x, icon_y))
