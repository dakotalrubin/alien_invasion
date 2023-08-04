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
        self.ship_speed = 1.5