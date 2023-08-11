# Author: Dakota Rubin
# Date: August 6th, 2023
# File: scoreboard.py contains all scoring info for the Alien Invasion game.

import pygame.font
from pygame.sprite import Group
from ship import Ship

"""This class contains all scorekeeping for Alien Invasion."""
class Scoreboard:

    """Initialize scorekeeping attributes."""
    def __init__(self, game):

        # Store game, screen, settings and stats info
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.stats = game.stats

        # Font settings for scorekeeping information
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Load all scoring system info to the screen
        self.prep_images()

    """Prepare score, high score, level and ship images for display."""
    def prep_images(self):

        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    """Render score image."""
    def prep_score(self):

        # Turn score string into a rendered image
        rounded_score = round(self.stats.score, -1)
        score_string = "Score: " + f"{rounded_score:,}"
        self.score_image = self.font.render(score_string, True,
            self.text_color, None)

        # Position score image at the top-right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    """Render high score image."""
    def prep_high_score(self):

        # Turn high score string into a rendered image
        rounded_high_score = round(self.stats.high_score, -1)
        high_score_string = "High Score: " + f"{rounded_high_score:,}"
        self.high_score_image = self.font.render(high_score_string, True,
            self.text_color, None)

        # Position high score image at the top-middle of the screen
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
            self.text_color, None)

        # Position level image at the top-right of the screen below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    """Show remaining number of lives."""
    def prep_ships(self):

        # Turn lives string into a rendered image
        lives_string = "Lives: "
        self.lives_image = self.font.render(lives_string, True,
            self.text_color, None)

        # Position lives image at the top-left of the screen
        self.lives_rect = self.lives_image.get_rect()
        self.lives_rect.left = self.screen_rect.left + 20
        self.lives_rect.top = 20

        self.ships = Group()

        # Create ship sprites and position them after lives image
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.game)
            ship.rect.x = self.lives_rect.right + (ship_number * ship.rect.width)
            ship.rect.y = 10
            self.ships.add(ship)

    """Draw score, high score, level and remaining lives to the screen."""
    def show_score(self):

        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.lives_image, self.lives_rect)
        self.ships.draw(self.screen)