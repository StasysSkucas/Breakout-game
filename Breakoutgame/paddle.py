import pygame
from settings import GameSettings


class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./assets/paddle.png").convert_alpha()
        self.rect = self.image.get_rect(center=(480, 500))
        self.paddle_velocity = 0
        self.speed = 500
        self.dt = 0

    def update(self):
        
        self.dt = GameSettings.dt
        
        # Handle input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.paddle_velocity = -self.speed
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.paddle_velocity = self.speed
        else:
            self.paddle_velocity = 0

        # Update position
        self.rect.x += self.paddle_velocity * self.dt

        # Keep paddle within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 960:
            self.rect.right = 960
