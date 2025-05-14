# status.py
import pygame
from enum import Enum
from config_loader import CONFIG


class status(Enum):
    ATTENTE = 1
    TRAITEMENT = 2
    EXPEDIEE = 3

    def __init__(self, value):
        if value == 1:
            self.label = "En attente"
            self.color = CONFIG["colors"]["red"]
        elif value == 2:
            self.label = "En traitement"
            self.color = CONFIG["colors"]["yellow"]
        elif value == 3:
            self.label = "Expédiée"
            self.color = CONFIG["colors"]["green"]

    def next_status(self):
        if self.value == 1:
            return status.TRAITEMENT
        elif self.value == 2:
            return status.EXPEDIEE
        elif self.value == 3:
            return self

    def draw_status_circle(self, surface, x, y):
        pygame.draw.circle(surface, self.color, (x, y), 10)

