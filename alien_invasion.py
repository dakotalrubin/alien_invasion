# Author: Dakota Rubin
# Date: August 3rd, 2023
# File: alien_invasion.py contains everything related to running the game.

import sys, pygame
from settings import Settings
from ship import Ship
from bullet import Bullet

"""This class manages game assets and behavior."""
class AlienInvasion:

    """Initialize game and create resources."""
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # Create a Ship instance using the current instance of AlienInvasion
        self.ship = Ship(self)

        # Create a sprite group to contain active bullets on-screen
        self.bullets = pygame.sprite.Group()

    """Run main game loop."""
    def run_game(self):
        while True:
            self.check_events()
            self.ship.update() # Update player ship position
            self.bullets.update() # Update active bullet positions
            self.update_screen()
            self.clock.tick(60) # Game runs at 60 frames per second

    """Listen for keypress and mouse events."""
    def check_events(self):
        for event in pygame.event.get():

            # Check if player wants to quit game
            if event.type == pygame.QUIT:
                sys.exit()

            # Check if player pressed a key
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)

            # Check if player released a key
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)

    """Listen for key presses."""
    def check_keydown_events(self, event):

        # Check if 'q' key pressed to quit game
        if event.key == pygame.K_q:
            sys.exit()

        # Check if right arrow key pressed
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True

        # Check if left arrow key pressed
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True

        # Check if spacebar pressed
        elif event.key == pygame.K_SPACE:
            self.fire_bullet()

    """Listen for key releases."""
    def check_keyup_events(self, event):
        # Check if right arrow key released
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

        # Check if left arrow key released
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    """Create new bullet and add to bullet group."""
    def fire_bullet(self):
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    """Update images on-screen and flip to new screen."""
    def update_screen(self):
        self.screen.fill(self.settings.bg_color)

        # Re-draw active bullets in group with updated positions
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.ship.blitme()
        pygame.display.flip()

if __name__ == '__main__':

    # Make a game instance and run game
    game = AlienInvasion()
    game.run_game()