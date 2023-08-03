# Author: Dakota Rubin
# Date: August 3rd, 2023
# File: ship.py contains all ship behavior for the Alien Invasion game.

import pygame

"""This class manages all ship behavior for Alien Invasion."""
class Ship:

    """Initialize the ship and set its starting position."""
    def __init__(self, game):
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()

        # Load the ship image and get its rectangle (sprite boundaries)
        self.image = pygame.image.load("images/ships/ship_002.png")
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom-center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

    """Draw the ship at its current location."""
    def blitme(self):
        self.screen.blit(self.image, self.rect)