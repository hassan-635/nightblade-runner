"""
Enemy entity for Nightblade-Runner.
Handles enemy AI, movement, and combat behavior.
"""

import pygame
import random
from utils.constants import (
    ENEMY_WIDTH, ENEMY_HEIGHT, ENEMY_BASE_SPEED, ENEMY_JUMP_STRENGTH,
    ENEMY_GRAVITY, WINDOW_WIDTH, WINDOW_HEIGHT,
    PLAYER_GROUND_Y, RED, ORANGE, YELLOW
)
from utils.sprite_loader import SpriteLoader


class Enemy:
    """
    Enemy ninja character.
    AI-controlled, moves toward player and attacks.
    """
    
    def __init__(self, x: int, y: int, speed: float = None):
        """
        Initialize the enemy.
        
        Args:
            x: Starting x position
            y: Starting y position
            speed: Movement speed (uses base speed if None)
        """
        # Position and movement
        self.x = float(x)
        self.y = float(y)
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.on_ground = False
        
        # AI settings
        self.speed = speed if speed is not None else ENEMY_BASE_SPEED
        self.detection_range = 3000  # Distance to detect player (effectively global)
        self.attack_range = 60  # Distance to attack player
        # Enemies don't jump - only run and idle
        
        # State management
        self.state = "idle"  # idle, run (no jumping)
        self.facing_right = True
        self.target_x = None  # Target x position (player position)
        
        # Combat
        self.health = 1  # Enemies die in one hit
        self.attack_cooldown = 0
        
        # Create rectangle for collision detection
        self.rect = pygame.Rect(int(self.x), int(self.y), ENEMY_WIDTH, ENEMY_HEIGHT)
        
        # Animation frame
        self.animation_frame = 0.0
        
        # Load sprites for different states
        self.sprite_loader = SpriteLoader()
        self.sprites = {
            "idle": self.sprite_loader.load_image(
                "assets/images/enemy/idle/idle.gif",
                (ENEMY_WIDTH, ENEMY_HEIGHT)
            ),
            "run": self.sprite_loader.load_image(
                "assets/images/enemy/run/run.gif",
                (ENEMY_WIDTH, ENEMY_HEIGHT)
            ),
            "jump": self.sprite_loader.load_image(
                "assets/images/enemy/jump/jump.gif",
                (ENEMY_WIDTH, ENEMY_HEIGHT)
            )
        }
    
    def update(self, player_pos: tuple, dt: float):
        """
        Update enemy AI and movement.
        
        Args:
            player_pos: (x, y) position of the player
            dt: Delta time for frame-rate independence
        """
        player_x, player_y = player_pos
        
        # Calculate distance to player
        distance_to_player = abs(self.x - player_x)
        
        # Reset horizontal velocity
        self.velocity_x = 0
        
        # AI: Move toward player if within detection range
        if distance_to_player < self.detection_range:
            if self.x < player_x:
                self.velocity_x = self.speed
                self.facing_right = True
                if self.on_ground:
                    self.state = "run"
            elif self.x > player_x:
                self.velocity_x = -self.speed
                self.facing_right = False
                if self.on_ground:
                    self.state = "run"
            else:
                # Close enough, stop moving
                if self.on_ground:
                    self.state = "idle"
        else:
            # Too far, idle
            if self.on_ground:
                self.state = "idle"
        
        # Enemies don't jump - they stay on ground
        # Keep them always on ground
        self.velocity_y = 0
        self.on_ground = True
        
        # Update position (only horizontal movement)
        self.x += self.velocity_x * dt
        
        # Keep enemy on ground level
        self.y = PLAYER_GROUND_Y
        
        # Keep enemy on screen horizontally
        self.x = max(0, min(self.x, WINDOW_WIDTH - ENEMY_WIDTH))
        
        # Update rectangle for collision detection
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
        # Update animation frame
        self.animation_frame += dt * 10
    
    def take_damage(self, amount: int = 1):
        """
        Apply damage to the enemy.
        
        Args:
            amount: Damage amount (default 1)
        """
        self.health -= amount
        if self.health < 0:
            self.health = 0
    
    def is_alive(self) -> bool:
        """
        Check if enemy is still alive.
        
        Returns:
            True if health > 0, False otherwise
        """
        return self.health > 0
    
    def draw(self, screen: pygame.Surface):
        """
        Draw the enemy on screen using sprite images.
        
        Args:
            screen: Pygame surface to draw on
        """
        # Get the sprite for current state (fallback to idle if not found)
        sprite = self.sprites.get(self.state, self.sprites.get("idle"))
        
        if sprite:
            # Flip sprite horizontally if facing left
            if not self.facing_right:
                sprite = pygame.transform.flip(sprite, True, False)
            
            # Draw the sprite
            screen.blit(sprite, self.rect)
        else:
            # Fallback to colored rectangle if sprite not loaded
            color = RED
            if self.state == "run":
                color = (255, 100, 100)  # Lighter red when running
            # Enemies don't jump, so no jump color needed
            pygame.draw.rect(screen, color, self.rect)

