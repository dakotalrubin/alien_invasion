# Author: Dakota Rubin
# Date: August 3rd, 2023
# File: ship.py contains all ship behavior for the Alien Invasion game.

import pygame
from pygame.sprite import Sprite

"""This class manages all ship behavior for Alien Invasion."""
class Ship(Sprite):

    """Initialize the ship and set its starting position."""
    def __init__(self, game):

        super().__init__()
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.settings = game.settings

        # Load ship image and get its sprite dimensions
        self.image = pygame.image.load("../images/sprites/ship.png")
        self.rect = self.image.get_rect()
        self.center_ship()

        # Movement flags (start with a ship that's not moving)
        self.moving_right = False
        self.moving_left = False

    """Update the ship's position based on movement flags."""
    def update(self):

        # Update the ship's x value
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Update rect object from self.x
        self.rect.x = self.x

    """Draw the ship at its current location."""
    def blitme(self):
        self.screen.blit(self.image, self.rect)

    """Center the ship on-screen."""
    def center_ship(self):

        # Start each new ship at the bottom-center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a float for the ship's horizontal position
        self.x = float(self.rect.x)