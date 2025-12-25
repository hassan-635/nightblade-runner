"""
Nightblade-Runner - Main Entry Point
A 2D ninja action game built with Python and Pygame.
"""

import pygame
import sys
from utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, WINDOW_TITLE, BLACK
from scenes.splash_screen import SplashScreen
from scenes.main_menu import MainMenu
from scenes.game_scene import GameScene


class Game:
    """
    Main game class that manages scenes and game loop.
    """
    
    def __init__(self):
        """Initialize the game."""
        # Initialize Pygame
        pygame.init()
        
        # Initialize mixer for audio
        pygame.mixer.init()
        
        # Create window
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        
        # Game clock for frame rate control
        self.clock = pygame.time.Clock()
        
        # Load and play background music
        self._load_background_music()
        
        # Current scene
        self.current_scene = "splash_screen"
        
        # Initialize scenes
        self.scenes = {
            "splash_screen": SplashScreen(),
            "main_menu": MainMenu(),
            "game_scene": GameScene()
        }
        
        # Running flag
        self.running = True
        
        # Initialize current scene
        self.scenes[self.current_scene].start()
    
    def _load_background_music(self):
        """Load and start playing background music."""
        try:
            music_path = "assets/audio/music.mp3"
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.5)  # Set volume to 50%
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
        except pygame.error as e:
            print(f"Warning: Could not load background music: {e}")
            print("Game will continue without music.")
    
    def run(self):
        """Main game loop."""
        last_time = pygame.time.get_ticks()
        
        while self.running:
            # Calculate delta time for frame-rate independent movement
            current_time = pygame.time.get_ticks()
            dt = (current_time - last_time) / 16.67  # Normalize to 60 FPS
            dt = min(dt, 2.0)  # Cap delta time to prevent large jumps
            last_time = current_time
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                
                # Let current scene handle event
                result = self.scenes[self.current_scene].handle_event(event)
                if result and result[0]:  # Check if result exists and has a scene name
                    next_scene, data = result
                    if next_scene == "exit":
                        self.running = False
                        break
                    elif next_scene:
                        self._change_scene(next_scene, data)
            
            # Update current scene
            result = self.scenes[self.current_scene].update(dt)
            if result and result[0]:  # Check if result exists and has a scene name
                next_scene, data = result
                if next_scene:
                    self._change_scene(next_scene, data)
            
            # Draw current scene
            self.scenes[self.current_scene].draw(self.screen)
            
            # Update display
            pygame.display.flip()
            
            # Control frame rate
            self.clock.tick(FPS)
        
        # Cleanup
        pygame.quit()
        sys.exit()
    
    def _change_scene(self, scene_name: str, data: dict = None):
        """
        Change to a different scene.
        
        Args:
            scene_name: Name of the scene to switch to
            data: Optional data to pass to the scene's start() method
        """
        if scene_name not in self.scenes:
            print(f"Warning: Scene '{scene_name}' not found!")
            return
        
        # Start the new scene with provided data
        if data:
            # Handle different scene start signatures
            if scene_name == "game_scene":
                level = data.get("level", 0)
                action = data.get("action", "new_game")
                self.scenes[scene_name].start(level=level, action=action)
            else:
                self.scenes[scene_name].start()
        else:
            self.scenes[scene_name].start()
        
        self.current_scene = scene_name


def main():
    """
    Entry point for the game.
    Creates and runs the game instance.
    """
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
