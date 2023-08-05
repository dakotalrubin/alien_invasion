# Author: Dakota Rubin
# Date: August 3rd, 2023
# File: settings.py contains all user settings for the Alien Invasion game.

"""This class stores all user settings for Alien Invasion."""
class Settings:

    """Initialize game settings."""
    def __init__(self):

        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (107, 73, 132)

        # Ship settings
        self.ship_speed = 4.0

        # Bullet settings
        self.bullet_speed = 6.0
        self.bullet_width = 3
        self.bullet_height = 20
        self.bullet_color = (247, 35, 49)
        self.bullets_allowed = 8

        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10

        # fleet_direction of 1 means right, fleet_direction of -1 means left
        self.fleet_direction = 1