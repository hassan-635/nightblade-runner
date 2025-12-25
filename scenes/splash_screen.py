"""
Splash Screen scene for Nightblade-Runner.
Shows animated title and transitions to main menu.
"""

import pygame
from utils.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, BLACK, WHITE, SPLASH_DURATION, FPS
)
from utils.sprite_loader import SpriteLoader


class SplashScreen:
    """
    Splash screen with animated title.
    Auto-transitions to main menu after a delay.
    """
    
    def __init__(self):
        """Initialize the splash screen."""
        self.start_time = None
        self.alpha = 0  # For fade-in effect
        self.fade_speed = 3  # Alpha increase per frame
        
        # Title text settings
        self.title_font = None
        self.title_text = "Nightblade-Runner"
        self.title_surface = None
        self.title_rect = None
        
        # Load background
        self.sprite_loader = SpriteLoader()
        self.background = None
    
    def start(self):
        """Called when scene becomes active."""
        self.start_time = pygame.time.get_ticks()
        self.alpha = 0
        
        # Load background
        self.background = self.sprite_loader.get_background(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Initialize font (using default font if pygame.font not initialized)
        try:
            self.title_font = pygame.font.Font(None, 72)
        except:
            # Fallback if font system not ready
            pass
    
    def update(self, dt: float) -> tuple:
        """
        Update splash screen animation.
        
        Args:
            dt: Delta time (unused but kept for consistency)
            
        Returns:
            Tuple of (next_scene, data) when ready, (None, None) to continue
        """
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.start_time if self.start_time else 0
        
        # Fade in effect
        if self.alpha < 255:
            self.alpha = min(255, self.alpha + self.fade_speed)
        
        # Auto-transition to main menu after delay
        if elapsed >= SPLASH_DURATION:
            return ("main_menu", None)
        
        return (None, None)
    
    def handle_event(self, event: pygame.event.Event) -> tuple:
        """
        Handle user input events.
        Allows skipping splash screen with any key or mouse click.
        
        Args:
            event: Pygame event object
            
        Returns:
            Tuple of (next_scene, data) if transition needed, (None, None) otherwise
        """
        # Allow skipping with any key or mouse click
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            return ("main_menu", None)
        
        return (None, None)
    
    def draw(self, screen: pygame.Surface):
        """
        Draw the splash screen.
        
        Args:
            screen: Pygame surface to draw on
        """
        # Draw background
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill(BLACK)
        
        # Draw title with fade-in effect
        if self.title_font:
            # Create text surface with alpha
            title_surface = self.title_font.render(
                self.title_text, True, WHITE
            )
            title_surface.set_alpha(self.alpha)
            
            # Center the title
            title_rect = title_surface.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
            )
            screen.blit(title_surface, title_rect)
        else:
            # Fallback: draw simple text
            font = pygame.font.Font(None, 72)
            title_surface = font.render(self.title_text, True, WHITE)
            title_surface.set_alpha(self.alpha)
            title_rect = title_surface.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
            )
            screen.blit(title_surface, title_rect)
        
        # Draw subtitle hint (fade in later)
        if self.alpha > 128:
            subtitle_font = pygame.font.Font(None, 24)
            subtitle_text = "Press any key to continue..."
            subtitle_surface = subtitle_font.render(
                subtitle_text, True, (200, 200, 200)
            )
            subtitle_surface.set_alpha(min(255, (self.alpha - 128) * 2))
            subtitle_rect = subtitle_surface.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80)
            )
            screen.blit(subtitle_surface, subtitle_rect)

