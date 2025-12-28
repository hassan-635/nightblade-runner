"""
Helper utility functions for Nightblade-Runner.
Contains reusable functions for common game operations.
"""

import json
import os
from typing import Dict, Any


def load_savegame(filepath: str) -> Dict[str, Any]:
    """
    Load game save data from JSON file.
    
    Args:
        filepath: Path to the savegame JSON file
        
    Returns:
        Dictionary containing save data, or default values if file doesn't exist
    """
    default_save = {
        "level": 0,
        "player_health": 100,
        "enemies_defeated": 0
    }
    
    if not os.path.exists(filepath):
        return default_save
    
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            return data
    except (json.JSONDecodeError, IOError):
        # If file is corrupted or can't be read, return default
        return default_save


def save_savegame(filepath: str, level: int, player_health: int, enemies_defeated: int) -> bool:
    """
    Save game progress to JSON file.
    
    Args:
        filepath: Path to save the JSON file
        level: Current level number
        player_health: Current player health
        enemies_defeated: Total enemies defeated
        
    Returns:
        True if save was successful, False otherwise
    """
    save_data = {
        "level": level,
        "player_health": player_health,
        "enemies_defeated": enemies_defeated
    }
    
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(save_data, f, indent=2)
        return True
    except IOError:
        return False


def clamp(value: float, min_value: float, max_value: float) -> float:
    """
    Clamp a value between min and max.
    
    Args:
        value: Value to clamp
        min_value: Minimum allowed value
        max_value: Maximum allowed value
        
    Returns:
        Clamped value
    """
    return max(min_value, min(value, max_value))


def check_collision(rect1, rect2) -> bool:
    """
    Check if two rectangles are colliding.
    
    Args:
        rect1: First pygame.Rect object
        rect2: Second pygame.Rect object
        
    Returns:
        True if rectangles overlap, False otherwise
    """
    return rect1.colliderect(rect2)


def distance(pos1: tuple, pos2: tuple) -> float:
    """
    Calculate Euclidean distance between two points.
    
    Args:
        pos1: First position (x, y)
        pos2: Second position (x, y)
        
    Returns:
        Distance as float
    """
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

