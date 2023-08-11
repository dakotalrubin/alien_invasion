# Author: Dakota Rubin
# Date: August 11th, 2023
# File: block.py contains all block behavior for the Alien Invasion game.

import pygame
from pygame.sprite import Sprite

"""This class manages all block behavior for Alien Invasion."""
class Block(Sprite):

    """Initialize the block and get its rect coordinates."""
    def __init__(self, size, color, x_position, y_position):

        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = (x_position, y_position))

shape = [
    "   xxxxxxxxxxxx",
    "  xxxxxxxxxxxxxx",
    " xxxxxxxxxxxxxxxx",
    "xxxxxxxxxxxxxxxxxx",
    "xxxxxx      xxxxxx",
    "xxxx          xxxx",
    "xxx            xxx"]