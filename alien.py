# Author: Dakota Rubin
# Date: August 5th, 2023
# File: alien.py contains all alien behavior for the Alien Invasion game.

import pygame
from pygame.sprite import Sprite

"""This class manages all alien behavior for Alien Invasion."""
class Alien(Sprite):

    """Initialize an alien and set its starting position."""
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen

        # Load the alien image and get its rectangle (sprite boundaries)
        self.image = pygame.image.load("images/ships/ship_017.png")
        self.rect = self.image.get_rect()

        # Start each new alien at the top-left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store a float for an alien's horizontal position
        self.x = float(self.rect.x)