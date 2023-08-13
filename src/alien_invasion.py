# Author: Dakota Rubin
# Date: August 3rd, 2023
# File: alien_invasion.py contains everything related to running the game.

import sys, pygame
from pygame import mixer
from random import choice

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from text_box import TextBox
from ship import Ship
from bullet import Bullet
from alien import Alien
from alien_bullet import AlienBullet
from explosion import Explosion
import block

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
        self.background = pygame.image.load("../images/background/background.png")
        pygame.display.set_caption("Alien Invasion")

        # Store game stats and scorekeeping info
        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)

        # Create a sprite group to contain player ship
        self.ship = Ship(self)
        self.ship_group = pygame.sprite.Group()

        # Create a sprite group to contain active bullets and alien bullets
        self.bullets = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()

        # Create a sprite group to contain all blocks
        self.shape = block.shape
        self.block_size = 8
        self.blocks = pygame.sprite.Group()
        self.create_multiple_blocks(0, 680)

        # Create a sprite group to contain active aliens
        self.aliens = pygame.sprite.Group()

        # Create a sprite group to contain explosions
        self.explosions = pygame.sprite.Group()

        # Create custom event for firing alien bullets
        self.alien_bullet_event = pygame.USEREVENT + 1

        # Game starts from inactive state
        self.game_active = False

        # Create variable to track whether fire button is being held
        self.holding_fire = False

        # Create variable to update time for latest fired bullet
        self.latest_fired_bullet = 0
        
        # Create variable to track delay between auto-fired bullets
        self.firing_delay = 200

        # Create variable to briefly pause the game after losing a life
        self.pause_game = False

        # Create variable to keep rendering the player ship when an alien
        # reaches the bottom of the screen
        self.alien_at_bottom = False

        # Create all menu buttons and text boxes
        self.create_menu_ui()

    """Run main game loop."""
    def run_game(self):

        while True:

            # Check for player input
            self.check_events()

            # Fire bullets at steady rate when fire button is being held
            if self.holding_fire:
                self.auto_fire_bullet()

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
    def start_round(self, mode, alien_firing_speed):

        # Hide mouse cursor
        pygame.mouse.set_visible(False)

        # Reset game statistics and change game state to active
        self.stats.reset_stats()
        self.scoreboard.prep_images()
        self.game_active = True

        # Load dynamic settings for easy, medium or hard difficulty
        self.settings.initialize_dynamic_settings(mode)
        pygame.time.set_timer(self.alien_bullet_event, alien_firing_speed)

        # Remove all remaining bullets, aliens and alien bullets
        self.bullets.empty()
        self.aliens.empty()
        self.alien_bullets.empty()

        # Create new alien fleet, new blocks and center player ship
        self.create_fleet()
        self.create_multiple_blocks(0, 680)
        self.ship_group.add(self.ship)
        self.ship.center_ship()

    """Remove all remaining bullets, create new game objects and increase speed."""
    def start_new_level(self):

        self.bullets.empty()
        self.alien_bullets.empty()
        self.create_fleet()
        self.ship_group.add(self.ship)
        self.settings.increase_speed()

        # Increment level and update display
        self.stats.level += 1
        self.scoreboard.prep_level()

    """Briefly pause the game if the player lost a life."""
    def check_pause(self):

        if self.pause_game:

            # Pause game so player has visual feedback for losing a life
            pygame.time.delay(500)
            self.pause_game = False
            self.alien_at_bottom = False

            # Remove all active bullets and alien bullets
            self.bullets.empty()
            self.alien_bullets.empty()

            # Update and draw new player ship and alien fleet
            self.ship.center_ship()
            self.ship_group.draw(self.screen)
            self.aliens.empty()
            self.create_fleet()
            self.aliens.draw(self.screen)
            pygame.display.flip()

    """Load all game music and sound effects."""
    def load_sounds(self):

        # Load music and loop indefinitely
        mixer.music.load("../sounds/song.mp3")
        mixer.music.set_volume(0.75)
        mixer.music.play(-1)

        # Load all sound effects
        self.boom_sound = pygame.mixer.Sound("../sounds/boom.wav")
        self.boom_sound.set_volume(0.27)
        self.bullet_sound = pygame.mixer.Sound("../sounds/bullet.wav")
        self.bullet_sound.set_volume(0.26)
        self.alien_bullet_sound = pygame.mixer.Sound("../sounds/alien_bullet.wav")
        self.alien_bullet_sound.set_volume(0.25)
        self.blip_sound = pygame.mixer.Sound("../sounds/blip.wav")
        self.blip_sound.set_volume(0.45)
        self.shield_down_sound = pygame.mixer.Sound("../sounds/shield_down.wav")
        self.shield_down_sound.set_volume(0.35)
        self.lost_life_sound = pygame.mixer.Sound("../sounds/lost_life.wav")
        self.lost_life_sound.set_volume(0.5)

    """Create menu buttons and text boxes."""
    def create_menu_ui(self):

        # Calculate center button coordinates
        center_button_x = (self.settings.screen_width / 2) - 100
        center_button_y = (self.settings.screen_height / 2) - 25

        # Create title text box with given attributes
        self.title_text_box = TextBox(self, "Alien Invasion", (0, 0, 255),
            (255, 255, 255), 480, 100,
            pygame.font.Font("../font/8_bit_madness.ttf", 72),
            center_button_x - 140, center_button_y - 120)

        # Create play buttons with given text, colors and coordinates
        self.easy_mode_button = Button(self, "Easy", (0, 255, 0),
            center_button_x - 210, center_button_y)
        self.medium_mode_button = Button(self, "Medium", (255, 255, 0),
            center_button_x, center_button_y)
        self.hard_mode_button = Button(self, "Hard", (255, 0, 0),
            center_button_x + 210, center_button_y)

        # Load menu controls image
        self.controls_image = pygame.image.load("../images/menu/controls.png")

    """Listen for keypress and mouse events."""
    def check_events(self):

        for event in pygame.event.get():

            # Check if it's time for alien to fire bullet
            if event.type == self.alien_bullet_event:
                self.fire_alien_bullet()

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
        # Start round on selected difficulty level with given alien firing speed
        if not self.game_active:

            if self.easy_mode_button.rect.collidepoint(mouse_pos):
                self.start_round("easy", 1200)

            elif self.medium_mode_button.rect.collidepoint(mouse_pos):
                self.start_round("medium", 1000)

            elif self.hard_mode_button.rect.collidepoint(mouse_pos):
                self.start_round("hard", 800)

    """Listen for key presses."""
    def check_keydown_events(self, event):

        # Check if "q" key or "Escape" key has been pressed to quit game
        if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:

            # Write high score to "high_score.txt" file
            with open("../user_data/high_score.txt", "w") as file:
                file.write(f"{self.stats.high_score}")

            pygame.quit()
            sys.exit()

        # Check if "p" key has been pressed while game state inactive
        # Play round on medium difficulty by default
        if event.key == pygame.K_p and not self.game_active:
            self.start_round("medium", 1000)

        # Check if spacebar has been pressed while game state inactive
        # Play round on medium difficulty by default
        elif event.key == pygame.K_SPACE and not self.game_active:
            self.start_round("medium", 1000)

        # Check if right arrow key has been pressed
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True

        # Check if left arrow key has been pressed
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True

        # Check if spacebar has been pressed while game state active
        elif event.key == pygame.K_SPACE and self.game_active:

            self.holding_fire = True
            self.fire_bullet()

    """Listen for key releases."""
    def check_keyup_events(self, event):

        # Check if right arrow key has been released
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

        # Check if left arrow key has been released
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        
        # Check if space bar has been released
        elif event.key == pygame.K_SPACE:
            self.holding_fire = False

    """Update images on-screen and flip to new screen."""
    def update_screen(self):

        self.screen.blit(self.background, (0, 0))

        # Re-draw blocks with updated shapes
        self.blocks.draw(self.screen)

        # Re-draw active bullets with updated positions
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Re-draw active alien bullets with updated positions
        for alien_bullet in self.alien_bullets.sprites():
            alien_bullet.draw_bullet()

        # Re-draw player ship if it hasn't been destroyed
        if self.alien_at_bottom or not self.pause_game:
            self.ship_group.draw(self.screen)

        # Draw alien fleet, explosions and score information
        self.aliens.draw(self.screen)
        self.explosions.draw(self.screen)
        self.scoreboard.show_score()

        # Draw title box, play buttons and controls image if game state inactive
        if not self.game_active:

            self.title_text_box.draw_text_box()
            self.easy_mode_button.draw_button()
            self.medium_mode_button.draw_button()
            self.hard_mode_button.draw_button()
            self.screen.blit(self.controls_image, (238, 445))

        pygame.display.flip()

        # Briefly pause after updating game objects if player lost a life
        self.check_pause()

# ------------------------------------------------------------------------------
# HELPER FUNCTIONS -------------------------------------------------------------
# ------------------------------------------------------------------------------

    """Create new block between player and alien fleet."""
    def create_block(self, x_start, y_start, x_offset):

        # Iterate through rows and columns to make a block
        for row_index, row in enumerate(self.shape):
            for column_index, column in enumerate(row):

                # Create individual parts of a block
                if column == "x":

                    x_position = x_start + ((column_index * self.block_size)
                        + x_offset)
                    y_position = y_start + (row_index * self.block_size)

                    block_object = block.Block(self.block_size, (0, 255, 255),
                        x_position, y_position)
                    self.blocks.add(block_object)

    """Create new blocks between player and alien fleet."""
    def create_multiple_blocks(self, x_start, y_start):

        # Create row of 4 evenly-spaced blocks on the screen
        for i in range(1, 5):
            self.create_block(x_start, y_start, (i * 256) - ((4 - i) * 49))

    """Create new bullet and add to bullet group (if allowed)."""
    def fire_bullet(self):

        # Allow player a maximum of 8 bullets on-screen at a time
        if len(self.bullets) < self.settings.bullet_limit:

            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

            # Update time for latest fired bullet
            self.latest_fired_bullet = pygame.time.get_ticks()

            # Play bullet sound when firing bullet
            mixer.Sound.play(self.bullet_sound)

    """Auto-fire new bullet if enough time has passed."""
    def auto_fire_bullet(self):

        # Calculate time since latest fired bullet
        time_since_latest_fired_bullet = (pygame.time.get_ticks() 
            - self.latest_fired_bullet)

        # Auto-fire new bullet after given delay
        if time_since_latest_fired_bullet >= self.firing_delay:
            self.fire_bullet()

    """Fire a bullet from a random alien ship."""
    def fire_alien_bullet(self):

        # Check to make sure at least one alien ship exists
        if self.aliens.sprites() and self.game_active:

            random_alien = choice(self.aliens.sprites())
            alien_bullet = AlienBullet(self, random_alien)
            self.alien_bullets.add(alien_bullet)

            # Play alien bullet sound when bullet spawns
            mixer.Sound.play(self.alien_bullet_sound)

    """Update bullet positions and despawn bullets that go off-screen."""
    def update_bullets(self):

        # Update bullet and alien bullet positions
        self.bullets.update()
        self.alien_bullets.update()

        # For loop needs list length to be constant, so loop over copy of list
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # Repeat procedure for alien bullets
        for alien_bullet in self.alien_bullets.copy():
            if alien_bullet.rect.top >= self.settings.screen_height:
                self.alien_bullets.remove(alien_bullet)

        # Check collisions between bullets and all game objects
        self.check_bullet_block_collisions()
        self.check_alien_bullet_block_collisions()
        self.check_bullet_alien_collisions()
        self.check_alien_bullet_ship_collisions()
        self.explosions.update()

    """Respond to bullet-block collisions."""
    def check_bullet_block_collisions(self):

        # Check for collisions between bullets and blocks
        # Remove colliding sprites
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.blocks, True, True)

        # If block(s) destroyed, play blip sound
        if collisions:
            mixer.Sound.play(self.blip_sound)

    """Respond to alien bullet-block collisions."""
    def check_alien_bullet_block_collisions(self):

        # Check for collisions between alien bullets and blocks
        # Remove colliding sprites
        collisions = pygame.sprite.groupcollide(
            self.alien_bullets, self.blocks, True, True)

        # If block(s) destroyed, play blip sound
        if collisions:
            mixer.Sound.play(self.blip_sound)

    """Respond to bullet-alien collisions."""
    def check_bullet_alien_collisions(self):

        # Check for collisions between bullets/aliens, remove colliding sprites
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        # If alien(s) destroyed, increment points, update score and
        # create explosion(s)
        if collisions:

            for aliens in collisions.values():

                # Increment score for every alien hit by single bullet
                self.stats.score += self.settings.alien_points * len(aliens)

                for alien in aliens:

                    # Replace alien sprite with explosion
                    explosion = Explosion(alien.rect.center)
                    self.explosions.add(explosion)

            # Play boom sound for alien hit
            mixer.Sound.play(self.boom_sound)

            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()

        if not self.aliens:
            self.start_new_level()

    """Respond to alien bullet-ship collisions."""
    def check_alien_bullet_ship_collisions(self):

        # Check for collisions between alien bullets and player ship
        if pygame.sprite.spritecollideany(self.ship, self.alien_bullets):

            # Replace player ship sprite with explosion
            self.ship_group.empty()
            explosion = Explosion(self.ship.rect.center)
            self.explosions.add(explosion)

            mixer.Sound.play(self.boom_sound)
            self.ship_hit()

    """Respond when an alien hits the player ship."""
    def ship_hit(self):

        mixer.Sound.play(self.lost_life_sound)

        # Decrement number of ships remaining and update scoreboard
        self.stats.ships_left -= 1
        self.scoreboard.prep_ships()

        if self.stats.ships_left > 0:

            # Add new player ship for rendering
            self.ship_group.add(self.ship)

            # Pause the game after losing a life
            self.pause_game = True

        # Game over, show mouse cursor for menu options
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    """Check if alien fleet at edge-of-screen, then update alien positions."""
    def update_aliens(self):

        self.check_fleet_edges()
        self.aliens.update()

        # Check for aliens colliding with blocks
        for alien in self.aliens:

            # Destroy blocks and play shield down sound
            if pygame.sprite.spritecollide(alien, self.blocks, True):
                mixer.Sound.play(self.shield_down_sound)

        # Check for aliens colliding with the player ship
        if pygame.sprite.spritecollideany(self.ship, self.aliens):

            # Replace player ship sprite with explosion
            self.ship_group.empty()
            explosion = Explosion(self.ship.rect.center)
            self.explosions.add(explosion)

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
        current_x, current_y = alien_width, alien_height + 72

        # Keep generating aliens in rows and columns until running out of room
        while current_y < self.settings.screen_height - (alien_height * 7):
            while current_x < (self.settings.screen_width - (alien_width * 2)):

                self.create_alien(current_x, current_y)
                current_x += alien_width * 2

            # Finished spawning a row of aliens
            # Reset x-coordinate and increment y-coordinate
            current_x = alien_width
            current_y += alien_height * 1.5

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

        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self.alien_reached_bottom()
                break

    """Respond when an alien reaches the bottom of the screen."""
    def alien_reached_bottom(self):

        # Keep rendering player ship sprite since it wasn't destroyed
        self.alien_at_bottom = True

        # Play lost life sound when an alien reaches the bottom the of screen
        mixer.Sound.play(self.lost_life_sound)

        # Decrement number of ships remaining and update scoreboard
        self.stats.ships_left -= 1
        self.scoreboard.prep_ships()

        if self.stats.ships_left > 0:

            # Pause the game after losing a life
            self.pause_game = True

        # Game over, show mouse cursor for menu options
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

if __name__ == '__main__':

    game = AlienInvasion()
    game.run_game()