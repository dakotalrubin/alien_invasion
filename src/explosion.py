# Author: Dakota Rubin
# Date: August 13th, 2023
# File: explosion.py contains all explosion behavior for the Alien Invasion game.

import pygame
from pygame.sprite import Sprite

"""This class manages all explosion behavior for Alien Invasion."""
class Explosion(Sprite):

    """Initialize an explosion and set its starting position."""
    def __init__(self, center):

        super().__init__()

        # Get explosion sprite dimensions
        self.image = pygame.image.load("../images/sprites/explosion.png")
        self.rect = self.image.get_rect()
        self.rect.center = center

        self.start_timer = pygame.time.get_ticks()

    """Remove explosion sprite after the given amount of time."""
    def update(self):

        # Display explosion sprite for 40 ms
        current_time = pygame.time.get_ticks()
        display_time = 40

        if current_time > self.start_timer + display_time:
            self.kill()