# text_edit.py
import pygame
from config_loader import CONFIG

font = pygame.font.Font(None, CONFIG["ui"]["font_size"])

class text_edit:
    def __init__(self, x, y, title=""):
        self.x = x
        self.y = y
        self.text = ""
        self.largeur = 200
        self.hauteur = 30
        self.title = title
        self.active = False
        self.color = CONFIG["colors"]["black"]
        self.rect = pygame.Rect(x, y + 20, self.largeur, self.hauteur)
        self.title_text = font.render(self.title, True, CONFIG["colors"]["black"])

    def draw(self, screen):
        screen.blit(self.title_text, (self.x, self.y))
        pygame.draw.rect(screen, self.color, self.rect, 2)
        input_text = font.render(self.text, True, CONFIG["colors"]["black"])
        screen.blit(input_text, (self.rect.x + 5, self.rect.y + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                # On ajoute le texte seulement si c'est un chiffre ou un point
                if event.unicode.isdigit() or (event.unicode == '.' and '.' not in self.text):
                    self.text += event.unicode 
                    

