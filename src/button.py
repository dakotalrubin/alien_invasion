# Author: Dakota Rubin
# Date: August 6th, 2023
# File: button.py contains all button behavior for the Alien Invasion game.

import pygame.font

"""This class manages all button behavior for Alien Invasion."""
class Button:

    """Initialize button attributes."""
    def __init__(self, game, message, button_color, x_position=0, y_position=0):

        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        # Set button dimensions and properties
        self.width, self.height = 200, 50
        self.button_color = button_color
        self.text_color = (0, 0, 0)
        self.font = pygame.font.Font("../font/8_bit_madness.ttf", 48)

        # Build button rect, center button, space button along x-axis
        self.rect = pygame.Rect(0, 0, self.width, self.height)

        # Set button position
        self.rect.x = x_position
        self.rect.y = y_position

        # Prep button message once
        self.prep_message(message)

    """Turn message into a rendered image and center text on button."""
    def prep_message(self, message):

        self.message_image = self.font.render(message, True,
            self.text_color, self.button_color)
        self.message_image_rect = self.message_image.get_rect()
        self.message_image_rect.center = self.rect.center

    """Draw blank button, then draw message."""
    def draw_button(self):

        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.message_image, self.message_image_rect)