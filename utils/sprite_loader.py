"""
Sprite loader utility for Nightblade-Runner.
Handles loading and caching of game sprites.
"""

import pygame
import os
from typing import Dict, Optional


class SpriteLoader:
    """
    Singleton class to load and cache sprites.
    Prevents loading the same image multiple times.
    """
    
    _instance = None
    _sprites: Dict[str, pygame.Surface] = {}
    
    def __new__(cls):
        """Create singleton instance."""
        if cls._instance is None:
            cls._instance = super(SpriteLoader, cls).__new__(cls)
        return cls._instance
    
    def load_image(self, filepath: str, scale: Optional[tuple] = None) -> Optional[pygame.Surface]:
        """
        Load an image file, with optional scaling.
        Caches loaded images to avoid reloading.
        
        Args:
            filepath: Path to the image file
            scale: Optional (width, height) tuple to scale the image
            
        Returns:
            Pygame Surface with the image, or None if loading failed
        """
        # Use filepath as cache key
        cache_key = f"{filepath}_{scale}" if scale else filepath
        
        # Return cached image if available
        if cache_key in self._sprites:
            return self._sprites[cache_key]
        
        # Try to load the image
        if not os.path.exists(filepath):
            print(f"Warning: Image file not found: {filepath}")
            return None
        
        try:
            image = pygame.image.load(filepath)
            # Convert to format that's faster to blit
            image = image.convert_alpha()
            
            # Scale if requested
            if scale:
                image = pygame.transform.scale(image, scale)
            
            # Cache the image
            self._sprites[cache_key] = image
            return image
        except pygame.error as e:
            print(f"Error loading image {filepath}: {e}")
            return None
    
    def get_background(self, width: int, height: int) -> Optional[pygame.Surface]:
        """
        Load and scale background image to fit screen.
        
        Args:
            width: Screen width
            height: Screen height
            
        Returns:
            Scaled background surface
        """
        bg_path = "assets/images/background/Landscape.gif"
        bg = self.load_image(bg_path)
        if bg:
            # Scale to fit screen while maintaining aspect ratio
            bg = pygame.transform.scale(bg, (width, height))
        return bg
    
    def clear_cache(self):
        """Clear the sprite cache (useful for memory management)."""
        self._sprites.clear()


# Convenience function for easy access
def load_sprite(filepath: str, scale: Optional[tuple] = None) -> Optional[pygame.Surface]:
    """
    Convenience function to load a sprite.
    
    Args:
        filepath: Path to the image file
        scale: Optional (width, height) tuple to scale the image
        
    Returns:
        Pygame Surface with the image, or None if loading failed
    """
    loader = SpriteLoader()
    return loader.load_image(filepath, scale)

