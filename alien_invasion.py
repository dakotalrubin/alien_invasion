# Author: Dakota Rubin
# Date: August 3rd, 2023
# File: alien_invasion.py contains everything related to running the game.

import sys, pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

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

        # Create a sprite group to contain active aliens on-screen
        self.aliens = pygame.sprite.Group()
        self.create_fleet()

    """Run main game loop."""
    def run_game(self):

        while True:

            # Check for player input
            self.check_events()

            # Update game object positions
            self.ship.update()
            self.update_bullets()
            self.update_aliens()

            # Draw new screen with current game object positions
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

    """Create new bullet and add to bullet group if allowed."""
    def fire_bullet(self):

        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    """Update bullet positions and despawn bullets that go off-screen."""
    def update_bullets(self):

        # Update bullet positions
        self.bullets.update()

        # For loop needs list length to be constant, so loop over copy of list
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    """Check if fleet at edge-of-screen, then update alien positions."""
    def update_aliens(self):
        self.check_fleet_edges()
        self.aliens.update()

    """Create a fleet of aliens."""
    def create_fleet(self):

        # Create space around aliens equal to one alien size
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        # The x-coordinate and y-coordinate of the next alien to spawn
        current_x, current_y = alien_width, alien_height

        # Create alien and keep adding aliens until there's no room left
        while current_y < (self.settings.screen_height - (alien_height * 3)):
            while current_x < (self.settings.screen_width - (alien_width * 2)):
                self.create_alien(current_x, current_y)
                current_x += alien_width * 2

            # Finished spawning a row of aliens
            # Reset x-coordinate and increment y-coordinate
            current_x = alien_width
            current_y += alien_height * 2

    """Create alien and add to row."""
    def create_alien(self, x_position, y_position):

        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    """Respond properly if an alien reaches left or right edge of screen."""
    def check_fleet_edges(self):

        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    """Drop fleet down the screen and change fleet direction."""
    def change_fleet_direction(self):

        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed

        self.settings.fleet_direction *= -1

    """Update images on-screen and flip to new screen."""
    def update_screen(self):

        self.screen.fill(self.settings.bg_color)

        # Re-draw active bullets with updated positions
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Re-draw ship and alien fleet with updated positions
        self.ship.blitme()
        self.aliens.draw(self.screen)
        pygame.display.flip()

if __name__ == '__main__':

    # Make a game instance and run game
    game = AlienInvasion()
    game.run_game()