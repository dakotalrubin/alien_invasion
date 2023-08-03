# Author: Dakota Rubin
# Date: August 3rd, 2023
# File: alien_invasion.py contains everything related to running the game.

import sys
import pygame
from settings import Settings
from ship import Ship

"""This class manages game assets and behavior."""
class AlienInvasion:

    """Initialize game and create resources."""
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Create a Ship instance using the current instance of AlienInvasion
        self.ship = Ship(self)

    """Start main game loop."""
    def run_game(self):
        while True:

            # Listen for keyboard and mouse events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # Redraw the screen during each pass through the loop
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()

            # Make the most recently-drawn screen visible
            pygame.display.flip()
            self.clock.tick(60) # Game runs at 60 frames per second

if __name__ == '__main__':

    # Make a game instance and run game
    game = AlienInvasion()
    game.run_game()