"""
Player entity for Nightblade-Runner.
Handles player movement, animation states, and combat.
"""

import pygame
from utils.constants import (
    PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED, PLAYER_JUMP_STRENGTH,
    PLAYER_GRAVITY, PLAYER_GROUND_Y, WINDOW_WIDTH, WINDOW_HEIGHT,
    ATTACK_RANGE, ATTACK_COOLDOWN, PLAYER_HEALTH, RED, GREEN, BLUE, WHITE
)
from utils.sprite_loader import SpriteLoader


class Player:
    """
    Player ninja character.
    Can idle, run, jump, and attack enemies.
    """
    
    def __init__(self, x: int, y: int):
        """
        Initialize the player.
        
        Args:
            x: Starting x position
            y: Starting y position
        """
        # Position and movement
        self.x = float(x)
        self.y = float(y)
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.on_ground = False
        
        # State management
        self.state = "idle"  # idle, run, jump
        self.facing_right = True  # Direction player is facing
        
        # Combat
        self.health = PLAYER_HEALTH
        self.max_health = PLAYER_HEALTH
        self.attack_cooldown = 0  # Milliseconds remaining until can attack again
        
        # Dash mechanics
        self.dash_cooldown = 0
        self.dash_time = 0
        self.is_dashing = False
        self.dash_speed = PLAYER_SPEED * 2.5
        
        # Create rectangle for collision detection
        self.rect = pygame.Rect(int(self.x), int(self.y), PLAYER_WIDTH, PLAYER_HEIGHT)
        
        # Animation frame (for future sprite animation)
        self.animation_frame = 0.0
        
        # Load sprites for different states
        self.sprite_loader = SpriteLoader()
        self.sprites = {
            "idle": self.sprite_loader.load_image(
                "assets/images/player/idle/idle.gif",
                (PLAYER_WIDTH, PLAYER_HEIGHT)
            ),
            "run": self.sprite_loader.load_image(
                "assets/images/player/run/run.gif",
                (PLAYER_WIDTH, PLAYER_HEIGHT)
            ),
            "jump": self.sprite_loader.load_image(
                "assets/images/player/jump/jump.gif",
                (PLAYER_WIDTH, PLAYER_HEIGHT)
            )
        }
    
    def update(self, keys: pygame.key.ScancodeWrapper, dt: float):
        """
        Update player state based on input and time.
        
        Args:
            keys: Pygame keys object for input detection
            dt: Delta time (time since last frame) for frame-rate independence
        """
        # Update dash timers
        if self.dash_cooldown > 0:
            self.dash_cooldown -= dt * 1000
        
        if self.is_dashing:
            self.dash_time -= dt * 1000
            if self.dash_time <= 0:
                self.is_dashing = False
                self.velocity_x = 0 # Stop dashing sliding
        
        # Handle Dash Input
        if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and self.dash_cooldown <= 0 and not self.is_dashing:
            self.start_dash()

        # If dashing, override movement
        if self.is_dashing:
            self.velocity_x = self.dash_speed if self.facing_right else -self.dash_speed
            self.velocity_y = 0 # Defy gravity while dashing
            
            # Update position (Dash)
            self.x += self.velocity_x * dt
            
            # Keep player on screen horizontally
            self.x = max(0, min(self.x, WINDOW_WIDTH - PLAYER_WIDTH))
            
            # Update rectangle
            self.rect.x = int(self.x)
            self.rect.y = int(self.y)
            return # Skip normal movement/gravity

        # Normal Movement Logic...
        
        # Reset horizontal velocity
        self.velocity_x = 0
        
        # Handle horizontal movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity_x = -PLAYER_SPEED
            self.facing_right = False
            if self.on_ground:
                self.state = "run"
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity_x = PLAYER_SPEED
            self.facing_right = True
            if self.on_ground:
                self.state = "run"
        else:
            if self.on_ground:
                self.state = "idle"
        
        # Handle jumping (Space is reserved for attack, so only Up/W keys)
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.velocity_y = PLAYER_JUMP_STRENGTH
            self.on_ground = False
            self.state = "jump"
        
        # Apply gravity
        if not self.on_ground:
            self.velocity_y += PLAYER_GRAVITY
            self.state = "jump"
        
        # Update position
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        
        # Ground collision
        if self.y >= PLAYER_GROUND_Y:
            self.y = PLAYER_GROUND_Y
            self.velocity_y = 0
            self.on_ground = True
            if self.state == "jump":
                self.state = "idle"
        
        # Keep player on screen horizontally
        self.x = max(0, min(self.x, WINDOW_WIDTH - PLAYER_WIDTH))
        
        # Update rectangle for collision detection
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
        # Update attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt * 1000  # Convert dt to milliseconds
        
        # Update animation frame
        self.animation_frame += dt * 10  # Adjust speed as needed

    def start_dash(self):
        """Initiate a dash."""
        self.is_dashing = True
        self.dash_time = 200 # 200ms dash duration
        self.dash_cooldown = 1000 # 1 second cooldown
    
    def attack(self) -> bool:
        """
        Attempt to perform an attack.
        
        Returns:
            True if attack was performed, False if on cooldown
        """
        if self.attack_cooldown <= 0:
            self.attack_cooldown = ATTACK_COOLDOWN
            return True
        return False
    
    def get_attack_rect(self) -> pygame.Rect:
        """
        Get the rectangle representing the attack hitbox.
        
        Returns:
            Rectangle representing attack range
        """
        # Attack extends forward from player
        attack_x = self.x + PLAYER_WIDTH if self.facing_right else self.x - ATTACK_RANGE
        attack_y = self.y
        attack_width = ATTACK_RANGE
        attack_height = PLAYER_HEIGHT
        
        return pygame.Rect(int(attack_x), int(attack_y), attack_width, attack_height)
    
    def take_damage(self, amount: int):
        """
        Apply damage to the player.
        
        Args:
            amount: Damage amount
        """
        if self.is_dashing: return # Invincible while dashing
        
        self.health -= amount
        if self.health < 0:
            self.health = 0
    
    def is_alive(self) -> bool:
        """
        Check if player is still alive.
        
        Returns:
            True if health > 0, False otherwise
        """
        return self.health > 0
    
    def draw(self, screen: pygame.Surface):
        """
        Draw the player on screen using sprite images.
        
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
            color = BLUE
            if self.is_dashing:
                color = WHITE # Visual cue for dash
            elif self.state == "jump":
                color = GREEN
            elif self.state == "run":
                color = (100, 150, 255)
            pygame.draw.rect(screen, color, self.rect)
        
        # Draw health bar above player
        bar_width = PLAYER_WIDTH
        bar_height = 5
        bar_x = self.rect.x
        bar_y = self.rect.y - 10
        
        # Background (red)
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        # Health (green)
        health_width = int(bar_width * (self.health / self.max_health))
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, health_width, bar_height))

