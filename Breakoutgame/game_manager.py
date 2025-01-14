import pygame
import ball



class GameManager:
    def __init__(self, paddle):
        self.game_started = False
        self.game_over = False
        self.victory = False
        self.ball_launched = False
        self.score = 0
        self.player_lives = 3
        self.ball = ball.Ball(self, paddle)
        self.paddle = paddle
        self.brick_group = None
        self.total_bricks = 0
        self.ball_group = pygame.sprite.Group()
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_delay = 1000 
        self.play_soundtrack()
        self.lose_life_sound = pygame.mixer.Sound('./assets/lost.wav')
        self.lose_life_sound.set_volume(0.5)
    
    def start_game(self):
        keys = pygame.key.get_pressed()
        if self.game_over:
            if keys[pygame.K_SPACE]:
                self.restart_game()
                return
        
        if not self.game_over:
            if keys[pygame.K_SPACE] and not self.game_started:
                self.game_started = True
            
            if keys[pygame.K_SPACE] and not self.ball_launched and self.game_started:
                self.ball_launched = True
                self.ball.launch_ball()
    
    def set_total_bricks(self, total_bricks):
        self.total_bricks = total_bricks

    
    def remove_brick(self):
        self.total_bricks -= 1
        if self.total_bricks == 0:
            self.victory = True
            self.finish_game()
        
    def add_score(self):
        self.score += 100

    def remove_live(self):
        self.player_lives -= 1

        self.lose_life_sound.play()
        self.lose_life_sound.play()
        if self.player_lives <= 0:
            self.finish_game()
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
        
    def play_soundtrack(self):
            pygame.mixer.music.load('./assets/soundtrack.mp3') 
            pygame.mixer.music.set_volume(0.3)  
            pygame.mixer.music.play(-1)  

        
    
    def draw_game_over(self, screen):

        font = "./assets/BitPotion.ttf"
        if self.game_over:
            center_x = screen.get_width() // 2
            center_y = screen.get_height() // 2
            spacing = 80  
            
            if not self.victory:
                game_over_text = pygame.font.Font(font, 74).render('GAME OVER', True, (255, 0, 0))
            else:
                game_over_text = pygame.font.Font(font, 74).render('VICTORY', True, (0, 255, 0))
            text_rect = game_over_text.get_rect(center=(center_x, center_y - spacing))
            screen.blit(game_over_text, text_rect)
            
            score_text = pygame.font.Font(font, 52).render(f'FINAL SCORE: {self.score}', True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(center_x, center_y))
            screen.blit(score_text, score_rect)
            
            restart_text = pygame.font.Font(font, 42).render('PRESS SPACE TO RESTART', True, (255, 255, 255))
            restart_rect = restart_text.get_rect(center=(center_x, center_y + spacing))
            screen.blit(restart_text, restart_rect)
            

        
        
    def finish_game(self):
        self.game_over = True
        if self.brick_group:
            self.brick_group.empty()
        
    
    def draw_game_start(self, screen):
        if not self.game_started:
            font = "./assets/BitPotion.ttf"
            center_x = screen.get_width() // 2
            center_y = screen.get_height() // 2
            spacing = 40

            # Make text larger and brighter
            controls_text = pygame.font.Font(font, 52).render('A / D TO CONTROL', True, (255, 255, 255))
            controls_rect = controls_text.get_rect(center=(center_x, center_y - spacing))
            screen.blit(controls_text, controls_rect)
            
            launch_text = pygame.font.Font(font, 52).render('SPACE TO LAUNCH', True, (255, 255, 255))
            launch_rect = launch_text.get_rect(center=(center_x, center_y + spacing))
            screen.blit(launch_text, launch_rect)
    


    
