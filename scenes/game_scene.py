"""
Game Scene for Nightblade-Runner.
Main gameplay with endless combat and enemy management.
"""

import pygame
import random
import time
from entities.player import Player
from entities.enemy import Enemy
from utils.constants import (
    SAVEGAME_PATH, WINDOW_WIDTH, WINDOW_HEIGHT, BLACK, WHITE, GRAY, DARK_GRAY, GREEN,
    PLAYER_GROUND_Y, ENEMY_SPEED_INCREMENT,
    ENEMY_BASE_SPEED, ENEMY_SAFE_SPAWN_DISTANCE, RED, YELLOW
)
from utils.helpers import save_savegame, check_collision, distance
from utils.sprite_loader import SpriteLoader
from utils.particle_system import ParticleSystem


class GameScene:
    """
    Main game scene with endless combat.
    """
    
    def __init__(self):
        """Initialize the game scene."""
        self.player = None
        self.enemies = []
        
        # Endless mode stats
        self.score = 0  # Enemies defeated
        self.max_enemies_on_screen = 5
        self.spawn_timer = 0
        self.spawn_interval = 2000  # Spawn attempt every 2 seconds if under limit
        
        # Juice / Game Feel
        self.particle_system = ParticleSystem()
        self.screen_shake = 0
        self.hit_stop_duration = 0 # Frames to skip logic
        
        # Combo System
        self.combo_count = 0
        self.combo_timer = 0
        self.combo_timeout = 3000 # 3 seconds to keep combo
        
        # Game state
        self.paused = False
        self.game_over = False
        
        # Fonts
        self.font = None
        self.big_font = None
        self.combo_font = None
        
        # Load background
        self.sprite_loader = SpriteLoader()
        self.background = None
        
        # Background (simple colored background for now - fallback)
        self.background_color = (30, 30, 50)  # Dark blue-gray
        
        # Ground visualization
        self.ground_rect = pygame.Rect(
            0, PLAYER_GROUND_Y + 64, WINDOW_WIDTH, WINDOW_HEIGHT - PLAYER_GROUND_Y - 64
        )
    
    def start(self, level: int = 0, action: str = "new_game"):
        """
        Initialize or reset the game scene.
        
        Args:
            level: Ignored in endless mode, kept for compatibility
            action: "new_game" or "continue"
        """
        self.paused = False
        self.game_over = False
        self.screen_shake = 0
        self.combo_count = 0
        
        if action == "continue":
            # Load saved game
            from utils.helpers import load_savegame
            save_data = load_savegame(SAVEGAME_PATH)
            self.score = save_data.get("score", 0)  # Use "score" instead of "enemies_defeated"
            # Fallback for old save files that might use enemies_defeated_total
            if self.score == 0:
                 self.score = save_data.get("enemies_defeated", 0)
        else:
            # New game
            self.score = 0
        
        # Initialize fonts
        try:
            self.font = pygame.font.Font(None, 36)
            self.big_font = pygame.font.Font(None, 72)
            self.combo_font = pygame.font.Font(None, 96) # Big font for combos
        except:
            pass
        
        # Load background
        self.background = self.sprite_loader.get_background(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Create player at starting position
        player_start_x = WINDOW_WIDTH // 2  # Start in middle for endless
        player_start_y = PLAYER_GROUND_Y
        self.player = Player(player_start_x, player_start_y)
        
        # If continuing, restore player health from save
        if action == "continue":
            from utils.helpers import load_savegame
            save_data = load_savegame(SAVEGAME_PATH)
            self.player.health = save_data.get("player_health", 100)
        
        # Clear existing enemies
        self.enemies.clear()
        
        # Spawn initial enemies
        self._maintain_enemies()
    
    def _maintain_enemies(self):
        """Maintain a certain number of enemies on screen, spawning from different sides."""
        if len(self.enemies) < self.max_enemies_on_screen:
            self._spawn_single_enemy()

    def _spawn_single_enemy(self):
        """Spawn a single enemy from a random location."""
        # Calculate enemy speed based on score (difficulty progression)
        # Every 10 kills, enemies get slightly faster
        base_speed_multiplier = 1 + (self.score // 10) * 0.1
        
        # Add random variation to speed (some fast, some slow)
        # 0.8x (slow) to 1.3x (fast) variance
        speed_variance = random.uniform(0.8, 1.3)
        
        enemy_speed = ENEMY_BASE_SPEED * base_speed_multiplier * speed_variance
        
        # Get player position
        player_x = int(self.player.x) if self.player else WINDOW_WIDTH // 2
        
        # Randomly choose side (Left or Right)
        # 0 = Left, 1 = Right
        side = random.choice([0, 1])
        
        spawn_x = 0
        
        # Spawn from further away to allow for "continuous movement" feel from distance
        spawn_distance = random.randint(600, 1000)
        
        if side == 0: # Left
            spawn_x = player_x - spawn_distance
        else: # Right
            spawn_x = player_x + spawn_distance
            
        spawn_y = PLAYER_GROUND_Y
        
        enemy = Enemy(spawn_x, spawn_y, speed=enemy_speed)
        self.enemies.append(enemy)

    def update(self, dt: float) -> tuple:
        """
        Update game state.
        
        Args:
            dt: Delta time for frame-rate independence
            
        Returns:
            Tuple of (next_scene, data) if transition needed, (None, None) otherwise
        """
        # Don't update if paused or game over
        if self.paused or self.game_over:
            return (None, None)
        
        # Hit Stop - Skip logic update if frozen
        if self.hit_stop_duration > 0:
            self.hit_stop_duration -= 1
            # Still update particles during hit stop for dramatic effect? 
            # Or freeze them too? freezings implies impact.
            return (None, None)
        
        # Update Screen Shake
        if self.screen_shake > 0:
            self.screen_shake -= dt * 20 # Decay shake
            if self.screen_shake < 0: self.screen_shake = 0
            
        # Update Combo Timer
        if self.combo_count > 0:
            self.combo_timer -= dt * 1000
            if self.combo_timer <= 0:
                self.combo_count = 0
        
        # Update Particles
        self.particle_system.update(dt)
        
        # Get keyboard input
        keys = pygame.key.get_pressed()
        
        # Update player
        if self.player and self.player.is_alive():
            self.player.update(keys, dt)
            
            # Create dash particles
            if self.player.is_dashing and random.random() < 0.3:
                 self.particle_system.emit(
                     self.player.x + 20, self.player.y + 40, 
                     count=2, color=WHITE, speed=1, type="dust"
                 )
            
            # Handle attack (Space key) - kill enemy on collision
            if keys[pygame.K_SPACE] or keys[pygame.K_x]:
                if self.player.attack():
                    # Check if player collides with any enemy (only kill one enemy per attack)
                    for enemy in self.enemies:  # Iterate through enemies
                        if enemy.is_alive() and check_collision(self.player.get_attack_rect(), enemy.rect): # Use attack rect
                            # Kill enemy instantly on collision when space is pressed
                            enemy.take_damage(1)
                            if not enemy.is_alive():
                                self.score += 1
                                
                                # Juice: Screen Shake, Particles, Hit Stop
                                self.screen_shake = 10
                                self.particle_system.emit(enemy.x + enemy.rect.width//2, enemy.y + enemy.rect.height//2, count=20, color=RED, speed=8, type="blood")
                                self.hit_stop_duration = 3 # Freeze for 3 frames
                                
                                # Combo
                                self.combo_count += 1
                                self.combo_timer = self.combo_timeout
                                
                                # Health regeneration every 10 kills
                                if self.score > 0 and self.score % 10 == 0:
                                    # Add small health boost
                                    self.player.health = min(self.player.max_health, self.player.health + 10)
                                    # Visual juice for heal
                                    self.particle_system.emit(self.player.x, self.player.y, count=15, color=GREEN, speed=4, type="dust")
                                
                                # Spawn replacement immediately to keep pressure
                                self._spawn_single_enemy()
                                
                            break  # Only kill one enemy per attack
        
        # Update enemies
        if self.player and self.player.is_alive():
            player_pos = (self.player.x, self.player.y)
            for enemy in self.enemies:
                if enemy.is_alive():
                    enemy.update(player_pos, dt)
                    
                    # Check if enemy collides with player (enemy attacks player)
                    if check_collision(enemy.rect, self.player.rect):
                        # Simple damage on collision - health decreases slowly
                        # Invincible while dashing
                        if self.player.attack_cooldown <= 0 and not self.player.is_dashing:
                            self.player.take_damage(1)
                            self.player.attack_cooldown = 1200  # Invincibility frame
                            
                            # Player got hit juice
                            self.screen_shake = 5
                            self.particle_system.emit(self.player.x, self.player.y, count=5, color=RED, speed=3)
                            self.combo_count = 0 # Reset combo on hit
        
        # Remove dead enemies
        self.enemies = [e for e in self.enemies if e.is_alive()]
        
        # Periodically check to spawn more enemies if count is low
        self.spawn_timer += dt * 10 # Approx ms
        if self.spawn_timer > self.spawn_interval:
            self._maintain_enemies()
            self.spawn_timer = 0
            
            # Slowly increase limit as score goes up
            target_enemies = 3 + (self.score // 5)
            self.max_enemies_on_screen = min(target_enemies, 10) # Cap at 10 enemies
            
        # Check if player is dead
        if self.player and not self.player.is_alive():
            self.game_over = True
            # Save game over state
            save_savegame(SAVEGAME_PATH, 0, 100, self.score)
        
        return (None, None)
    
    def handle_event(self, event: pygame.event.Event) -> tuple:
        """
        Handle user input events.
        
        Args:
            event: Pygame event object
            
        Returns:
            Tuple of (next_scene, data) if transition needed, (None, None) otherwise
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Toggle pause
                self.paused = not self.paused
                if self.paused:
                    # When pausing, return to main menu
                    return ("main_menu", None)
            
            # Allow restart on game over
            if self.game_over and event.key == pygame.K_r:
                self.start(level=0, action="new_game")
        
        return (None, None)
    
    def draw(self, screen: pygame.Surface):
        """
        Draw the game scene.
        
        Args:
            screen: Pygame surface to draw on
        """
        # Apply Screen Shake offset
        shake_x = 0
        shake_y = 0
        if self.screen_shake > 0:
            shake_x = random.randint(int(-self.screen_shake), int(self.screen_shake))
            shake_y = random.randint(int(-self.screen_shake), int(self.screen_shake))
            
        # Create a surface to draw everything on, then blit with offset
        # OR just straight up act like the camera moved. 
        # Since this is a simple game without scrolling camera yet, we can't easily scroll.
        # But we can simulate shake by just modifying where we draw things.
        # Actually... `game_scene.draw` receives the main screen directly.
        # For simplicity, let's just create a temporary surface if we want full screen shake,
        # OR just off-set drawing positions. Off-setting everything is tedious.
        # EASIEST: Just blit background with offset, and offset all entities.
        
        # Draw background
        bg_x = shake_x
        bg_y = shake_y
        
        if self.background:
            screen.blit(self.background, (bg_x, bg_y))
        else:
            screen.fill(self.background_color) # Fill clean first functionality? No, fill invalidates shake.
            # If shaking, we might see black edges. That's fine for "Juice".
        
        # Draw ground
        ground_rect_shaken = self.ground_rect.copy()
        ground_rect_shaken.x += shake_x
        ground_rect_shaken.y += shake_y
        pygame.draw.rect(screen, DARK_GRAY, ground_rect_shaken)
        
        # Ground line
        pygame.draw.line(
            screen, GRAY,
            (0 + shake_x, PLAYER_GROUND_Y + 64 + shake_y),
            (WINDOW_WIDTH + shake_x, PLAYER_GROUND_Y + 64 + shake_y),
            3
        )
        
        # Save original positions to restore after drawing (hacky but works for simple objects)
        # Better: Pass an offset to draw methods? 
        # Player and Enemy `draw` use self.rect. 
        # Let's adjust self.rect temporarily? No, that messes up physics.
        # Ideally `draw` takes an offset. 
        # But I can't change all entities right now easily without updating them all.
        # WAIT. Entities draw to `screen` at `self.rect`.
        # I can create a subsurface or just accept that entities won't shake perfectly unless I change their draw.
        # Actually, let's update `draw` calls to use a blit offset?
        # Standard approach: Create a `game_surface`, draw everything there, then blit `game_surface` to `screen` with shake offset.
        
        game_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        if self.background:
             game_surface.blit(self.background, (0, 0))
        else:
             game_surface.fill(self.background_color)
             
        pygame.draw.rect(game_surface, DARK_GRAY, self.ground_rect)
        pygame.draw.line(game_surface, GRAY, (0, PLAYER_GROUND_Y+64), (WINDOW_WIDTH, PLAYER_GROUND_Y+64), 3)
        
        if self.player: self.player.draw(game_surface)
        for enemy in self.enemies: 
            if enemy.is_alive(): enemy.draw(game_surface)
            
        # Draw particles
        self.particle_system.draw(game_surface)
            
        # Blit game_surface to main screen with shake
        screen.blit(game_surface, (shake_x, shake_y))
        
        # Draw UI (on top of shake or with shake? usually static UI is better)
        self._draw_ui(screen)
        
        # Draw pause overlay
        if self.paused:
            self._draw_pause_overlay(screen)
        
        # Draw game over
        if self.game_over:
            self._draw_game_over(screen)
    
    def _draw_ui(self, screen: pygame.Surface):
        """Draw user interface elements."""
        if not self.font:
            self.font = pygame.font.Font(None, 36)
        
        # Score indicator (top left)
        score_text = f"Score: {self.score}"
        score_surface = self.font.render(score_text, True, WHITE)
        screen.blit(score_surface, (20, 20))
        
        # Combo Indicator!
        if self.combo_count > 1:
            scale = min(1.0 + (self.combo_count * 0.1), 2.0) # Cap scale at 2x
            if not self.combo_font: self.combo_font = pygame.font.Font(None, 60)
            
            combo_text = f"{self.combo_count} COMBO!"
            # Dynamic color
            color = YELLOW if self.combo_count < 10 else RED
            
            combo_surf = self.combo_font.render(combo_text, True, color)
            # Center top
            text_rect = combo_surf.get_rect(center=(WINDOW_WIDTH // 2, 100))
            screen.blit(combo_surf, text_rect)
            
            # Timer bar for combo
            bar_width = 200 * (self.combo_timer / self.combo_timeout)
            pygame.draw.rect(screen, color, (WINDOW_WIDTH // 2 - 100, 130, bar_width, 10))
        
        # Controls / Hints (bottom)
        if self.player and self.player.is_alive():
            instruction_font = pygame.font.Font(None, 24)
            # Dynamic hint based on score
            if self.score > 0 and self.score % 10 == 0:
                 hint = "Health Renewed!"
                 hint_color = GREEN
            else:
                 hint = "Shift: DASH | Space: ATTACK"
                 hint_color = GRAY
                 
            text_surface = instruction_font.render(hint, True, hint_color)
            text_rect = text_surface.get_rect(
                center=(WINDOW_WIDTH // 2, 50)
            )
            screen.blit(text_surface, text_rect)
    
    def _draw_pause_overlay(self, screen: pygame.Surface):
        """Draw pause screen overlay."""
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Pause text
        if not self.big_font:
            self.big_font = pygame.font.Font(None, 72)
        pause_text = self.big_font.render("PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        screen.blit(pause_text, pause_rect)
    
    def _draw_game_over(self, screen: pygame.Surface):
        """Draw game over screen."""
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Game over text
        if not self.big_font:
            self.big_font = pygame.font.Font(None, 72)
        game_over_text = self.big_font.render("GAME OVER", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        screen.blit(game_over_text, game_over_rect)
        
        # Stats
        if not self.font:
            self.font = pygame.font.Font(None, 36)
        stats_text = f"Final Score: {self.score}"
        stats_surface = self.font.render(stats_text, True, GRAY)
        stats_rect = stats_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
        screen.blit(stats_surface, stats_rect)
        
        # Restart instruction
        restart_text = self.font.render("Press R to Restart or ESC for Menu", True, GRAY)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80))
        screen.blit(restart_text, restart_rect)

