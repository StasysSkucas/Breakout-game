import pygame
import ball

class GameManager:
    def __init__(self, paddle):
        self.game_started = False
        self.game_over = False
        self.ball_launched = False
        self.score = 0
        self.player_lives = 3
        self.ball = ball.Ball(self, paddle)
        self.brick_group = None
        self.font = pygame.font.Font("./assets/BitPotion.ttf", 74)
         
    
    def start_game(self):
        keys = pygame.key.get_pressed()
        self.game_started = True
        if keys[pygame.K_SPACE] and not self.ball_launched and self.game_started:

            self.ball_launched = True
            self.ball.launch_ball()
    
    def add_score(self):
        self.score += 100

    def remove_live(self):

        self.player_lives -= 1
        if self.player_lives <= 0:
            self.end_game()
            return
        else:
            self.ball_launched = False
            self.ball.reset_ball()
    
    def restart_game(self):
        if self.game_over:
            self.game_over = False
            self.score = 0
            self.player_lives = 3
            self.ball.reset_ball()
            self.game_started = True
            self.ball_launched = False
            from brick import Brick
            Brick.create_grid(self.brick_group, self)

        
    def set_brick_group(self, brick_group):
        self.brick_group = brick_group
    
    def draw_game_over(self, screen):
        if self.game_over:
            game_over_text = self.font.render('GAME OVER', True, (255, 255, 255))
            text_rect = game_over_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 100))
            screen.blit(game_over_text, text_rect)
            
            score_text = self.font.render(f'FINAL SCORE: {self.score}', True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(score_text, score_rect)
            
            restart_text = self.font.render('PRESS SPACE TO RESTART', True, (255, 255, 255))
            restart_rect = restart_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100))
            screen.blit(restart_text, restart_rect)
            
    def end_game(self):
        self.game_over = True
        if self.brick_group:
            self.brick_group.empty()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.restart_game()
        
    


    
