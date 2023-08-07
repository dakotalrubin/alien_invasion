# Author: Dakota Rubin
# Date: August 6th, 2023
# File: scoreboard.py contains all scoring info for the Alien Invasion game.

import pygame.font

"""This class contains all scorekeeping for Alien Invasion."""
class Scoreboard:

    """Initialize scorekeeping attributes."""
    def __init__(self, game):

        # Store screen, settings and stats info
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.stats = game.stats

        # Font settings for scorekeeping information
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare score, high score and level images for display
        self.prep_score()
        self.prep_high_score()
        self.prep_level()

    """Render score image."""
    def prep_score(self):

        # Turn score string into a rendered image
        rounded_score = round(self.stats.score, -1)
        score_string = "Score: " + f"{rounded_score:,}"
        self.score_image = self.font.render(score_string, True,
            self.text_color, self.settings.bg_color)

        # Position score at the top-right of the screen with 20px margin
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    """Render high score image."""
    def prep_high_score(self):

        # Turn high score string into a rendered image
        rounded_high_score = round(self.stats.high_score, -1)
        high_score_string = "High Score: " + f"{rounded_high_score:,}"
        self.high_score_image = self.font.render(high_score_string, True,
            self.text_color, self.settings.bg_color)

        # Position high score at the top-middle of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    """Check for new high score."""
    def check_high_score(self):

        # Overwrite existing high score with new higher score
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    """Render level image."""
    def prep_level(self):

        # Turn level string into a rendered image
        level_string = "Level: " + str(self.stats.level)
        self.level_image = self.font.render(level_string, True,
            self.text_color, self.settings.bg_color)

        # Position level at the top-right of the screen below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 20

    """Draw score, high score and level to the screen."""
    def show_score(self):

        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)