# Author: Dakota Rubin
# Date: August 3rd, 2023
# File: alien_invasion.py contains everything related to running the game.

import sys, pygame
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
            self.check_events()
            self.ship.update() # Update player ship position
            self.update_screen()
            self.clock.tick(60) # Game runs at 60 frames per second

    """Listen for keypress and mouse events."""
    def check_events(self):
        for event in pygame.event.get():

            # Check if player exited the game window
            if event.type == pygame.QUIT:
                sys.exit()

            # Check if player pressed a key
            elif event.type == pygame.KEYDOWN:

                # Check if right arrow key pressed
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = True

                # Check if left arrow key pressed
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = True

            # Check if player released a key
            elif event.type == pygame.KEYUP:

                # Check if right arrow key released
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False

                # Check if left arrow key released
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False

    """Update images on-screen and flip to new screen."""
    def update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        pygame.display.flip()

if __name__ == '__main__':

    # Make a game instance and run game
    game = AlienInvasion()
    game.run_game()