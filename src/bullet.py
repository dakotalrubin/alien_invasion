# Author: Dakota Rubin
# Date: August 4th, 2023
# File: bullet.py contains all bullet behavior for the Alien Invasion game.

import pygame
from pygame.sprite import Sprite

"""This class manages all bullet behavior for Alien Invasion."""
class Bullet(Sprite):

    """Initialize bullet object at the ship's current position."""
    def __init__(self, game):

        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.color = self.settings.bullet_color

        # Create bullet sprite (rect) at top-left of screen (0, 0)
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
            self.settings.bullet_height)

        # Set bullet position to middle-top of ship
        self.rect.midtop = game.ship.rect.midtop

        # Store bullet position as float for more precise control
        self.y = float(self.rect.y)

    """Move the bullet up the screen."""
    def update(self):

        # Update bullet position (decrease the y-coordinate)
        self.y -= self.settings.bullet_speed

        # Update bullet sprite (rect) position
        self.rect.y = self.y

    """Draw the bullet's new position to the screen."""
    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)