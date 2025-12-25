"""
Main Menu scene for Nightblade-Runner.
Provides New Game, Continue, and Exit options.
"""

import pygame
from utils.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, BLACK, WHITE, GRAY, DARK_GRAY, GREEN, SAVEGAME_PATH
)
from utils.helpers import load_savegame
from utils.sprite_loader import SpriteLoader


class MainMenu:
    """
    Main menu with navigation options.
    """
    
    def __init__(self):
        """Initialize the main menu."""
        self.selected_option = 0  # Currently selected menu item
        self.menu_options = ["New Game", "Continue", "Exit"]
        self.font = None
        self.title_font = None
        
        # Load background
        self.sprite_loader = SpriteLoader()
        self.background = None
        
        # Check if save file exists for Continue option
        self.save_exists = False
        self.check_save_file()
    
    def check_save_file(self):
        """Check if a save file exists."""
        save_data = load_savegame(SAVEGAME_PATH)
        # Continue is available if level > 0 (game has been played)
        self.save_exists = save_data.get("level", 0) > 0
    
    def start(self):
        """Called when scene becomes active."""
        self.selected_option = 0
        self.check_save_file()  # Re-check in case save was created
        
        # Load background
        self.background = self.sprite_loader.get_background(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Initialize fonts
        try:
            self.title_font = pygame.font.Font(None, 64)
            self.font = pygame.font.Font(None, 48)
        except:
            pass
    
    def update(self, dt: float) -> tuple:
        """
        Update menu state.
        
        Args:
            dt: Delta time (unused but kept for consistency)
            
        Returns:
            Tuple of (next_scene, data) if transition needed, (None, None) otherwise
        """
        # Menu doesn't auto-update, only responds to input
        return (None, None)
    
    def handle_event(self, event: pygame.event.Event) -> tuple:
        """
        Handle user input events.
        
        Args:
            event: Pygame event object
            
        Returns:
            Tuple of (next_scene, data) where data is dict with action info
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                # Move selection up
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                # Skip Continue if save doesn't exist
                if self.selected_option == 1 and not self.save_exists:
                    self.selected_option = (self.selected_option - 1) % len(self.menu_options)
            
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                # Move selection down
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                # Skip Continue if save doesn't exist
                if self.selected_option == 1 and not self.save_exists:
                    self.selected_option = (self.selected_option + 1) % len(self.menu_options)
            
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                # Select option
                return self._select_option()
        
        return (None, None)
    
    def _select_option(self) -> tuple:
        """
        Handle option selection.
        
        Returns:
            Tuple of (next_scene, data) with action information
        """
        option = self.menu_options[self.selected_option]
        
        if option == "New Game":
            # Start new game from level 0
            return ("game_scene", {"action": "new_game", "level": 0})
        
        elif option == "Continue":
            if self.save_exists:
                # Load saved game
                save_data = load_savegame(SAVEGAME_PATH)
                level = save_data.get("level", 0)
                return ("game_scene", {"action": "continue", "level": level})
            # Shouldn't happen, but handle gracefully
            return (None, None)
        
        elif option == "Exit":
            # Return special signal to quit
            return ("exit", None)
        
        return (None, None)
    
    def draw(self, screen: pygame.Surface):
        """
        Draw the main menu.
        
        Args:
            screen: Pygame surface to draw on
        """
        # Draw background
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill(BLACK)
        
        # Draw title
        if self.title_font:
            title_surface = self.title_font.render(
                "Nightblade-Runner", True, WHITE
            )
        else:
            title_surface = pygame.font.Font(None, 64).render(
                "Nightblade-Runner", True, WHITE
            )
        title_rect = title_surface.get_rect(
            center=(WINDOW_WIDTH // 2, 150)
        )
        screen.blit(title_surface, title_rect)
        
        # Draw menu options
        if not self.font:
            self.font = pygame.font.Font(None, 48)
        
        start_y = 300
        spacing = 80
        
        for i, option in enumerate(self.menu_options):
            # Skip Continue if save doesn't exist
            if option == "Continue" and not self.save_exists:
                continue
            
            # Determine color based on selection
            if i == self.selected_option:
                color = GREEN
                # Draw selection indicator
                indicator_x = WINDOW_WIDTH // 2 - 200
                indicator_y = start_y + i * spacing + 20
                pygame.draw.circle(screen, GREEN, (indicator_x, indicator_y), 8)
            else:
                color = GRAY
            
            # Draw option text
            option_surface = self.font.render(option, True, color)
            option_rect = option_surface.get_rect(
                center=(WINDOW_WIDTH // 2, start_y + i * spacing)
            )
            screen.blit(option_surface, option_rect)
        
        # Draw instructions
        instruction_font = pygame.font.Font(None, 24)
        instructions = [
            "Use UP/DOWN or W/S to navigate",
            "Press ENTER or SPACE to select"
        ]
        for i, instruction in enumerate(instructions):
            text_surface = instruction_font.render(instruction, True, DARK_GRAY)
            text_rect = text_surface.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100 + i * 30)
            )
            screen.blit(text_surface, text_rect)

