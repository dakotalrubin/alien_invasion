# Author: Dakota Rubin
# Date: August 5th, 2023
# File: game_stats.py contains all statistics for the Alien Invasion game.

"""This class stores all statistics for Alien Invasion."""
class GameStats:

    """Initialize game statistics."""
    def __init__(self, game):

        self.settings = game.settings
        self.reset_stats()

    """Initialize stats that can change during a game."""
    def reset_stats(self):
        self.ships_left = self.settings.ship_limit