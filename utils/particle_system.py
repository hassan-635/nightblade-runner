"""
Particle System for Nightblade-Runner.
Handles visual effects like blood, dust, and sparks.
"""

import pygame
import random
from utils.constants import RED, WHITE, YELLOW, ORANGE

class Particle:
    """A single particle effect."""
    def __init__(self, x, y, color, velocity, lifetime, size=3):
        self.x = x
        self.y = y
        self.color = color
        self.velocity_x = velocity[0]
        self.velocity_y = velocity[1]
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = size
        self.gravity = 0.2

    def update(self, dt):
        """Update particle position and lifetime."""
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        self.velocity_y += self.gravity * dt # Apply gravity
        self.lifetime -= dt * 10 

    def draw(self, screen, scroll_x=0, scroll_y=0):
        """Draw the particle."""
        if self.lifetime > 0:
            # Fade out
            alpha = int((self.lifetime / self.max_lifetime) * 255)
            
            # Create a surface for transparency
            surf = pygame.Surface((self.size, self.size))
            surf.set_alpha(alpha)
            surf.fill(self.color)
            
            screen.blit(surf, (int(self.x - scroll_x), int(self.y - scroll_y)))

class ParticleSystem:
    """Manager for all particles."""
    def __init__(self):
        self.particles = []

    def emit(self, x, y, count=10, color=RED, speed=5, type="explosion"):
        """Emit a burst of particles."""
        for _ in range(count):
            angle = random.uniform(0, 3.14159 * 2)
            velocity_magnitude = random.uniform(1, speed)
            
            if type == "blood":
                # Blood sprays upwards mostly
                vx = random.uniform(-speed, speed)
                vy = random.uniform(-speed, -1)
            elif type == "dust":
                vx = random.uniform(-1, 1)
                vy = random.uniform(-0.5, 0.5)
            else:
                vx = random.uniform(-speed, speed)
                vy = random.uniform(-speed, speed)
            
            lifetime = random.uniform(20, 40)
            size = random.randint(2, 4)
            
            self.particles.append(Particle(x, y, color, (vx, vy), lifetime, size))

    def update(self, dt):
        """Update all particles."""
        for p in self.particles:
            p.update(dt)
        # Remove dead particles
        self.particles = [p for p in self.particles if p.lifetime > 0]

    def draw(self, screen, scroll_x=0, scroll_y=0):
        """Draw all particles."""
        for p in self.particles:
            p.draw(screen, scroll_x, scroll_y)
