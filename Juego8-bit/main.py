import pygame
import sys
from settings import *
from game_functions import game, game_over
from intro import intro

# Inicializar pygame
pygame.init()

# Configurar pantalla y reloj
screen = pygame.display.set_mode(res)
clock = pygame.time.Clock()

if __name__ == "__main__":
    intro(screen, clock)
