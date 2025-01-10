import pygame

from settings import GameSettings

class Ball(pygame.sprite.Sprite):
    def __init__(self, game_manager, paddle, ):  
        super().__init__()
        self.image = pygame.image.load("./assets/ball.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.velocity = [0, 0]
        self.speed = 20
        self.dt = 0
        self.game_manager = game_manager 
        self.paddle = paddle

    def launch_ball(self):
            self.velocity = [(self.paddle.paddle_velocity ), -self.speed ]

        
    def handle_paddle_collision(self):
        if self.rect.colliderect(self.paddle.rect):
            hit_position = (self.rect.centerx - self.paddle.rect.left) / self.paddle.rect.width
    
            if self.rect.top < self.paddle.rect.top: 
                self.velocity[1] = -abs(self.velocity[1]) 
                
                if hit_position < 0.33:
                    if self.velocity[0] == 0:
                        self.velocity[0] = -100
                    else:
                        self.velocity[0] = -abs(self.velocity[0])  
               
                elif hit_position > 0.67:
                    if self.velocity[0] == 0:
                        self.velocity[0] = 100
                    else: 
                        self.velocity[0] = abs(self.velocity[0]) 
            else:  
                self.velocity[0] = -self.velocity[0]
                
    def handle_ball_boundary(self):
        if self.rect.left <= 0:
            self.rect.left = 0 
            self.velocity[0] = abs(self.velocity[0]) 
        elif self.rect.right >= GameSettings.SCREEN_WIDTH:
            self.rect.right = GameSettings.SCREEN_WIDTH  
            self.velocity[0] = -abs(self.velocity[0])  
        if self.rect.top <= 0:
            self.rect.top = 0  
            self.velocity[1] = abs(self.velocity[1])
        elif self.rect.bottom >= GameSettings.SCREEN_HEIGHT:
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
                

            brick.on_hit()
            
    def update(self, brick_group):
        self.dt = GameSettings.dt
        if not self.game_manager.ball_launched:
            self.rect.centerx = self.paddle.rect.centerx
            self.rect.y = self.paddle.rect.top - self.rect.height
        else:
            self.rect.centerx += self.velocity[0]  * self.dt
            self.rect.centery += self.velocity[1] * self.speed * self.dt
            
        self.handle_ball_boundary()
        self.handle_paddle_collision()
        self.handle_brick_collision(brick_group) 
        
