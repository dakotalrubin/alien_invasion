# Author: Dakota Rubin
# Date: August 3rd, 2023
# File: alien_invasion.py contains everything related to running the game.

import sys
import pygame

"""Game class to manage assets and behavior."""
class AlienInvasion:

    """Initialize game and create resources."""
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Alien Invasion")

    """Start main game loop."""
    def run_game(self):
        while True:

            # Listen for keyboard and mouse events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # Make the most recently-drawn screen visible
            pygame.display.flip()

if __name__ == '__main__':

    # Make a game instance and run game
    game = AlienInvasion()
    game.run_game()