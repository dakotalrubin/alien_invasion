# Author: Dakota Rubin
# Date: August 5th, 2023
# File: alien.py contains all alien behavior for the Alien Invasion game.

import pygame
from pygame.sprite import Sprite
from random import choice

"""This class manages all alien behavior for Alien Invasion."""
class Alien(Sprite):

    """Initialize an alien and set its starting position."""
    def __init__(self, game):

        super().__init__()
        self.screen = game.screen
        self.settings = game.settings

        # Load a random alien sprite
        aliens = ["../images/sprites/alien1.png", "../images/sprites/alien2.png",
            "../images/sprites/alien3.png"]
        random_alien = choice(aliens)

        # Get alien sprite dimensions
        self.image = pygame.image.load(random_alien)
        self.rect = self.image.get_rect()

        # Start each new alien at the top-left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store float for an alien's horizontal position
        self.x = float(self.rect.x)

    """Return True if an alien hits the edge of the screen."""
    def check_edges(self):

        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    """Move an alien to the right or left."""
    def update(self):

        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x