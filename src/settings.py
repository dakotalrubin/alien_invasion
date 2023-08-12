# Author: Dakota Rubin
# Date: August 3rd, 2023
# File: settings.py contains all settings for the Alien Invasion game.

"""This class stores all settings for Alien Invasion."""
class Settings:

    """Initialize static game settings."""
    def __init__(self):

        # Screen settings
        self.screen_width = 1280
        self.screen_height = 800

        # Initial game difficulty
        self.mode = "medium"

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 20
        self.bullet_color = (0, 255, 0)
        self.bullet_limit = 8

        # Alien settings
        self.fleet_drop_speed = 10

        # Gameplay speed growth rate
        self.speedup_scale = 1.1

        # Alien point value growth rate
        self.score_scale = 1.5

        self.initialize_dynamic_settings(self.mode)

    """Initialize game settings that change over time."""
    def initialize_dynamic_settings(self, mode):

        # fleet_direction of 1 means right, fleet_direction of -1 means left
        self.fleet_direction = 1

        # Scoring settings
        self.alien_points = 50

        if mode == "easy":
            self.ship_speed = 4.0
            self.bullet_speed = 5.5
            self.alien_speed = 1.2
        elif mode == "medium":
            self.ship_speed = 5.0
            self.bullet_speed = 6.5
            self.alien_speed = 1.7
        elif mode == "hard":
            self.ship_speed = 6.0
            self.bullet_speed = 7.5
            self.alien_speed = 2.2

    """Increase game element speed and point value growth rate."""
    def increase_speed(self):

        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)