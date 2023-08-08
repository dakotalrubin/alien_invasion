# Author: Dakota Rubin
# Date: August 3rd, 2023
# File: alien_invasion.py contains everything related to running the game.

import sys, pygame
from pygame import mixer
from time import sleep

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from text_box import TextBox
from ship import Ship
from bullet import Bullet
from alien import Alien

"""This class manages game assets and behavior."""
class AlienInvasion:

    """Initialize game and create resources."""
    def __init__(self):

        pygame.init()

        # Initialize mixer and load audio files
        mixer.init()
        self.load_sounds()

        self.clock = pygame.time.Clock()

        # Store game settings
        self.settings = Settings()

        # Create game window with dimensions from settings.py
        self.screen = pygame.display.set_mode((
            self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Store game stats and scorekeeping info
        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)

        # Create a Ship instance using the current game instance
        self.ship = Ship(self)

        # Create a sprite group to contain active bullets on-screen
        self.bullets = pygame.sprite.Group()

        # Create a sprite group to contain active aliens on-screen
        self.aliens = pygame.sprite.Group()
        self.create_fleet()

        # Game starts from inactive state
        self.game_active = False

        # Create all menu buttons and text boxes
        self.create_menu_ui()

    """Run main game loop."""
    def run_game(self):

        while True:

            # Check for player input
            self.check_events()

            # If player has ships remaining
            if self.game_active:

                # Update game element positions
                self.ship.update()
                self.update_bullets()
                self.update_aliens()

            # Draw new screen with current game element positions
            self.update_screen()

            # Game runs at 60 frames per second
            self.clock.tick(60)

    """Start new round of Alien Invasion."""
    def start_game(self, mode):

        # Hide mouse cursor
        pygame.mouse.set_visible(False)

        # Reset game statistics and change game state to active
        self.stats.reset_stats()
        self.scoreboard.prep_images()
        self.game_active = True

        # Load dynamic settings for easy, medium or hard difficulty
        self.settings.initialize_dynamic_settings(mode)

        # Remove all remaining bullets and aliens
        self.bullets.empty()
        self.aliens.empty()

        # Create new alien fleet and center player ship
        self.create_fleet()
        self.ship.center_ship()

    """Load all game music and sound effects."""
    def load_sounds(self):

        # Load music and loop indefinitely
        # mixer.music.load("../sounds/song.wav")
        # mixer.music.set_volume(0.6)
        # mixer.music.play(-1)

        # Load boom, bullet and lost life sound effects
        self.boom_sound = pygame.mixer.Sound("../sounds/boom.wav")
        self.boom_sound.set_volume(0.26)
        self.bullet_sound = pygame.mixer.Sound("../sounds/bullet.wav")
        self.bullet_sound.set_volume(0.26)
        self.lost_life_sound = pygame.mixer.Sound("../sounds/lost_life.wav")
        self.lost_life_sound.set_volume(0.4)

    """Create menu buttons and text boxes."""
    def create_menu_ui(self):

        # Calculate center button coordinates
        center_button_x = (self.settings.screen_width / 2) - 100
        center_button_y = (self.settings.screen_height / 2) - 25

        # Create title text box with given attributes
        self.title_text_box = TextBox(self, "Alien Invasion", (0, 0, 255),
            (255, 255, 255), 400, 100, pygame.font.SysFont(None, 72),
            center_button_x - 100, center_button_y - 120)

        # Create play buttons with given text, colors and coordinates
        self.easy_mode_button = Button(self, "Easy", (0, 255, 0),
            center_button_x - 210, center_button_y)
        self.medium_mode_button = Button(self, "Medium", (255, 255, 0),
            center_button_x, center_button_y)
        self.hard_mode_button = Button(self, "Hard", (255, 0, 0),
            center_button_x + 210, center_button_y)

    """Listen for keypress and mouse events."""
    def check_events(self):

        for event in pygame.event.get():

            # Check if player pressed a key
            if event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)

            # Check if player released a key
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)

            # Check if player clicked mouse button
            elif event.type == pygame.MOUSEBUTTONDOWN:

                mouse_pos = pygame.mouse.get_pos()
                self.check_play_buttons(mouse_pos)

            # Check if player clicked the game window's quit button
            elif event.type == pygame.QUIT:

                # Write high score to "high_score.txt" file
                with open("../user_data/high_score.txt", "w") as file:
                    file.write(f"{self.stats.high_score}")

                pygame.quit()
                sys.exit()

    """Start new game when player clicks a play button."""
    def check_play_buttons(self, mouse_pos):

        # Check which play button has been clicked when game state inactive
        # Start game on the selected difficulty level
        if not self.game_active:

            if self.easy_mode_button.rect.collidepoint(mouse_pos):
                self.start_game("easy")

            elif self.medium_mode_button.rect.collidepoint(mouse_pos):
                self.start_game("medium")

            elif self.hard_mode_button.rect.collidepoint(mouse_pos):
                self.start_game("hard")

    """Listen for key presses."""
    def check_keydown_events(self, event):

        # Check if "q" key or "Escape" key pressed to quit game
        if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:

            # Write high score to "high_score.txt" file
            with open("../user_data/high_score.txt", "w") as file:
                file.write(f"{self.stats.high_score}")

            pygame.quit()
            sys.exit()

        # Check if "p" key has been pressed while game state inactive
        # Play game on medium difficulty by default
        if event.key == pygame.K_p and not self.game_active:
            self.start_game("medium")

        # Check if spacebar has been pressed while game state inactive
        # Play game on medium difficulty by default
        elif event.key == pygame.K_SPACE and not self.game_active:
            self.start_game("medium")

        # Check if right arrow key pressed
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True

        # Check if left arrow key pressed
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True

        # Check if spacebar pressed while game state active
        elif event.key == pygame.K_SPACE and self.game_active:
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

            # Play bullet sound when firing bullet
            mixer.Sound.play(self.bullet_sound)

    """Update bullet positions and despawn bullets that go off-screen."""
    def update_bullets(self):

        # Update bullet positions
        self.bullets.update()

        # For loop needs list length to be constant, so loop over copy of list
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self.check_bullet_alien_collisions()

    """Respond to bullet-alien collisions."""
    def check_bullet_alien_collisions(self):

        # Check for collisions between bullets/aliens, remove colliding sprites
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        # If alien(s) destroyed, increment points and create new score images
        if collisions:

            # Increment score for every alien hit by single bullet
            for aliens in collisions.values():

                self.stats.score += self.settings.alien_points * len(aliens)

            # Play boom sound for alien hit
            mixer.Sound.play(self.boom_sound)

            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()

        if not self.aliens:
            self.start_new_level()

    """Remove all remaining bullets, create new alien fleet and increase speed."""
    def start_new_level(self):

        self.bullets.empty()
        self.create_fleet()
        self.settings.increase_speed()

        # Increment level and update display
        self.stats.level += 1
        self.scoreboard.prep_level()

    """Respond when alien hits player ship or alien reaches bottom of screen."""
    def ship_hit(self):

        # Play lost life sound when alien hits ship or reaches bottom of screen
        mixer.Sound.play(self.lost_life_sound)

        if self.stats.ships_left > 0:

            # Decrement number of ships remaining and update scoreboard
            self.stats.ships_left -= 1
            self.scoreboard.prep_ships()

            # Remove all remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            # Create new alien fleet and center player ship
            self.create_fleet()
            self.ship.center_ship()

            # Wait half a second
            sleep(0.5)

        else:

            # Game over
            self.game_active = False

            # Show mouse cursor
            pygame.mouse.set_visible(True)

    """Check if alien fleet at edge-of-screen, then update alien positions."""
    def update_aliens(self):

        self.check_fleet_edges()
        self.aliens.update()

        # Check for alien collision with player ship
        if pygame.sprite.spritecollideany(self.ship, self.aliens):

            # Play boom sound for ship collision
            mixer.Sound.play(self.boom_sound)

            self.ship_hit()

        # Check for aliens hitting the bottom of the screen
        self.check_aliens_bottom()

    """Create a fleet of aliens."""
    def create_fleet(self):

        # Create space around aliens equal to one alien size
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        # The x-coordinate and y-coordinate of the next alien to spawn
        current_x, current_y = alien_width, alien_height + 92

        # Keep generating aliens in rows and columns until running out of room
        while current_y < self.settings.screen_height - (alien_height * 3):
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

    """Check if any aliens reach the bottom of the screen."""
    def check_aliens_bottom(self):

        # Treat this event the same as the player ship getting hit
        for alien in self.aliens.sprites():

            if alien.rect.bottom >= self.settings.screen_height:
                self.ship_hit()
                break

    """Update images on-screen and flip to new screen."""
    def update_screen(self):

        self.screen.fill(self.settings.bg_color)

        # Re-draw active bullets with updated positions
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Re-draw ship and alien fleet with updated positions
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Draw score information
        self.scoreboard.show_score()

        # Draw title text box and play buttons if game state inactive
        if not self.game_active:

            self.title_text_box.draw_text_box()
            self.easy_mode_button.draw_button()
            self.medium_mode_button.draw_button()
            self.hard_mode_button.draw_button()

        pygame.display.flip()

if __name__ == '__main__':

    # Make a game instance and run
    game = AlienInvasion()
    game.run_game()