# Author: Dakota Rubin
# Date: August 7th, 2023
# File: text_box.py contains all text box behavior for the Alien Invasion game.

import pygame.font

"""This class manages all text box behavior for Alien Invasion."""
class TextBox:

    """Initialize text box attributes."""
    def __init__(self, game, message, box_color, text_color, width, height,
        font, x_position=0, y_position=0):

        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        # Set text box dimensions and properties
        self.width, self.height = width, height
        self.box_color = box_color
        self.text_color = text_color
        self.font = font

        # Build text box rect
        self.rect = pygame.Rect(0, 0, self.width, self.height)

        # Set text box position
        self.rect.x = x_position
        self.rect.y = y_position

        # Prep text box message once
        self.prep_text_box_message(message)

    """Turn message into a rendered image and center text on text box."""
    def prep_text_box_message(self, message):

        self.message_image = self.font.render(message, True,
            self.text_color, self.box_color)
        self.message_image_rect = self.message_image.get_rect()
        self.message_image_rect.center = self.rect.center

    """Draw blank text box, then draw message."""
    def draw_text_box(self):

        self.screen.fill(self.box_color, self.rect)
        self.screen.blit(self.message_image, self.message_image_rect)