# Author: Dakota Rubin
# Date: August 12th, 2023
# File: alien_bullet.py contains all alien bullet behavior for Alien Invasion.

import pygame
from pygame.sprite import Sprite

"""This class manages all alien bullet behavior for Alien Invasion."""
class AlienBullet(Sprite):

    """Initialize alien bullet object at an alien's current position."""
    def __init__(self, game, alien):

        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.color = self.settings.alien_bullet_color

        # Create alien bullet sprite at top-left of screen (0, 0)
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
            self.settings.bullet_height)

        # Set alien bullet position to middle-bottom of alien ship
        self.rect.midtop = alien.rect.midbottom

        # Store alien bullet position as float for more precise control
        self.y = float(self.rect.y)

    """Move the alien bullet down the screen."""
    def update(self):

        # Update alien bullet position (increase the y-coordinate)
        self.y += self.settings.bullet_speed
        self.rect.y = self.y

    """Draw the alien bullet's new position to the screen."""
    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)