import pygame
import math
import random

from settings import GameSettings

class Ball(pygame.sprite.Sprite):
    def __init__(self, game_manager, paddle, ):  
        super().__init__()
        self.image = pygame.image.load("./assets/ball.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.velocity = [0, 0]
        self.speed = 22
        self.dt = 0
        self.game_manager = game_manager 
        self.paddle = paddle

    def launch_ball(self):
        if self.paddle.paddle_velocity == 0:
            self.velocity = [0, -self.speed] 
        else:
            direction = 1 if self.paddle.paddle_velocity > 0 else -1
            self.velocity = [direction * self.speed, -self.speed]

        
    def handle_paddle_collision(self):
        if self.rect.colliderect(self.paddle.rect):
            
            if self.game_manager.ball_launched == True:
                self.play_hit_sound()
            
            hit_position = (self.rect.centerx - self.paddle.rect.centerx) / (self.paddle.rect.width / 2)

            max_angle = math.pi / 3
            
            angle = hit_position * max_angle
            
            speed = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)
            self.velocity[0] = speed * math.sin(angle)
            self.velocity[1] = -abs(speed * math.cos(angle))  
                
    def handle_ball_boundary(self):
        if self.rect.left <= 0:
            self.rect.left = 0 
            self.velocity[0] = abs(self.velocity[0])
            self.play_hit_sound() 
        elif self.rect.right >= GameSettings.SCREEN_WIDTH:
            self.rect.right = GameSettings.SCREEN_WIDTH  
            self.velocity[0] = -abs(self.velocity[0])  
            self.play_hit_sound()
        if self.rect.top <= 0:
            self.rect.top = 0  
            self.velocity[1] = abs(self.velocity[1])
            self.play_hit_sound()
        elif self.rect.bottom >= GameSettings.SCREEN_HEIGHT and not self.game_manager.game_over:
            self.game_manager.remove_live()
            
   
                    
    def reset_ball(self):
        self.rect.centerx = self.paddle.rect.centerx
        self.rect.bottom = self.paddle.rect.top
        self.velocity = [0, 0]

        
    
        
    def handle_brick_collision(self, brick_group):
        
        collided_bricks = pygame.sprite.spritecollide(self, brick_group, False)
        
        if collided_bricks:
            brick = collided_bricks[0]  
            
            if self.rect.centerx < brick.rect.left or self.rect.centerx > brick.rect.right:
                self.velocity[0] *= -1  
            else:
                self.velocity[1] *= -1 
                
            self.play_hit_sound()
            brick.on_hit()
            
    def play_hit_sound(self):
        if not hasattr(self, 'hit_sounds'):
            self.hit_sounds = [
                pygame.mixer.Sound("./assets/hit1.wav"),  
                pygame.mixer.Sound("./assets/hit2.wav"),  
                pygame.mixer.Sound("./assets/hit3.wav"), 
            ]
        random.choice(self.hit_sounds).play()
        
    def update(self, brick_group):
        self.dt = GameSettings.dt
        if not self.game_manager.ball_launched:
            self.rect.centerx = self.paddle.rect.centerx
            self.rect.y = self.paddle.rect.top - self.rect.height
        else:
            self.rect.centerx += self.velocity[0]  * self.speed *self.dt
            self.rect.centery += self.velocity[1] * self.speed * self.dt
            
        self.handle_ball_boundary()
        self.handle_paddle_collision()
        self.handle_brick_collision(brick_group) 
        
