# Author: Dakota Rubin
# Date: August 6th, 2023
# File: scoreboard.py contains all scoring info for the Alien Invasion game.

import pygame.font

"""This class contains all scorekeeping for Alien Invasion."""
class Scoreboard:

    """Initialize scorekeeping attributes."""
    def __init__(self, game):

        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.stats = game.stats

        # Font settings for scorekeeping information
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare initialized score image
        self.prep_score()

    """Render score image."""
    def prep_score(self):

        # Render score image
        score_string = str(self.stats.score)
        self.score_image = self.font.render(score_string, True,
            self.text_color, self.settings.bg_color)

        # Position score at top-right of screen with 20px margin
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    """Draw score on-screen."""
    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)