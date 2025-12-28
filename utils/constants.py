"""
Constants for Nightblade-Runner game.
All game-wide constants are defined here for easy configuration.
"""

import pygame

# Window settings
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 60
WINDOW_TITLE = "Nightblade-Runner"

# Colors (RGB values)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Player settings
PLAYER_WIDTH = 96  # Increased from 64 - larger character
PLAYER_HEIGHT = 96  # Increased from 64 - larger character
PLAYER_SPEED = 5
PLAYER_JUMP_STRENGTH = -15
PLAYER_GRAVITY = 0.8
PLAYER_GROUND_Y = WINDOW_HEIGHT - PLAYER_HEIGHT - 50  # 50px from bottom

# Enemy settings
ENEMY_WIDTH = 96  # Increased from 64 - larger character
ENEMY_HEIGHT = 96  # Increased from 64 - larger character
ENEMY_BASE_SPEED = 1.0  # Reduced further - slower enemies
ENEMY_JUMP_STRENGTH = -12
ENEMY_GRAVITY = 0.8
ENEMY_SPAWN_DISTANCE = 100  # Distance from screen edge to spawn
ENEMY_SAFE_SPAWN_DISTANCE = 250  # Minimum distance from player to spawn (safe distance)

# Game settings
INITIAL_ENEMY_COUNT = 3  # Starting number of enemies per level
ENEMY_SPEED_INCREMENT = 0.2  # Further reduced - even slower speed increase per level
ENEMY_COUNT_INCREMENT = 1  # Additional enemies per level
LEVEL_COMPLETE_DELAY = 2000  # 2 seconds delay before next level (milliseconds)

# Combat settings
ATTACK_RANGE = 10  # Reduced to 10px for extreme close combat
ATTACK_COOLDOWN = 800  # Increased from 500 - slower sword motion
ENEMY_DAMAGE = 1
PLAYER_HEALTH = 100

# Animation settings
ANIMATION_SPEED = 0.2  # Lower = faster animation

# File paths
SAVEGAME_PATH = "data/savegame.json"
ASSETS_PATH = "assets"

# Scene transition settings
FADE_SPEED = 5  # Pixels per frame for fade effects
SPLASH_DURATION = 3000  # 3 seconds for splash screen

