# Author: Dakota Rubin
# Date: August 7th, 2023
# File: title.py contains all title box behavior for the Alien Invasion game.

import pygame.font

"""This class manages all title box behavior for Alien Invasion."""
class Title:

    """Initialize title attributes."""
    def __init__(self, game, message, box_color, text_color, width, height,
        font, x_position=0, y_position=0):

        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        # Set title dimensions and properties
        self.width, self.height = width, height
        self.box_color = box_color
        self.text_color = text_color
        self.font = font

        # Build title rect
        self.rect = pygame.Rect(0, 0, self.width, self.height)

        # Set title position
        self.rect.x = x_position
        self.rect.y = y_position

        # Prep button message once
        self.prep_title_message(message)

    """Turn message into a rendered image and center text on title box."""
    def prep_title_message(self, message):

        self.message_image = self.font.render(message, True,
            self.text_color, self.box_color)
        self.message_image_rect = self.message_image.get_rect()
        self.message_image_rect.center = self.rect.center

    """Draw blank title box, then draw message."""
    def draw_title_box(self):

        self.screen.fill(self.box_color, self.rect)
        self.screen.blit(self.message_image, self.message_image_rect)