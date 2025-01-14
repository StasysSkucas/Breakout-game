import pygame
import paddle
import brick

from settings import GameSettings
from game_manager import GameManager
from sys import exit

pygame.init()
GameSettings.initialize()
screen = GameSettings.SCREEN
pygame.display.set_caption("Breakout")
bg_surf = pygame.image.load("./assets/breakoutBG.jpg")


# Sprites
brick_group = pygame.sprite.Group()

paddle_group = pygame.sprite.GroupSingle()
ball_group = pygame.sprite.Group()

# Lives
lives_images = {
    3: pygame.image.load("./assets/Lives3.png").convert_alpha(),
    2: pygame.image.load("./assets/Lives2.png").convert_alpha(),
    1: pygame.image.load("./assets/Lives1.png").convert_alpha()
    
}

# Text
font = pygame.font.Font("./assets/BitPotion.ttf", 52)  
score_text = font.render("SCORE: 0", True, (255, 255, 255))  
score_rect = score_text.get_rect(topright=(GameSettings.SCREEN_WIDTH - 20, 20))

# Instances
player_paddle = paddle.Paddle()
game_manager = GameManager(player_paddle)
game_manager.set_brick_group(brick_group)
paddle_group.add(player_paddle)  
ball_group.add(game_manager.ball)

def create_bricks():
    brick_image = pygame.image.load("./assets/Brick1.png").convert_alpha()
    BRICK_WIDTH = brick_image.get_width()
    BRICK_HEIGHT = brick_image.get_height()
    for row in range(3):  
        for col in range(11):  
            x = col * (BRICK_WIDTH + 2) + 65  
            y = row * (BRICK_HEIGHT + 2) + 100
            new_brick = brick.Brick(x, y,  game_manager)
            brick_group.add(new_brick)
            

def draw_game():
    screen.blit(bg_surf, (0, 0))
    paddle_group.draw(screen)
    brick_group.draw(screen)
    ball_group.draw(screen)
    draw_lives()
    draw_score()
    game_manager.draw_game_start(screen)
    game_manager.draw_game_over(screen)
    pygame.display.update()

def draw_lives():
    if game_manager.player_lives > 0:
        lives_surf = lives_images[game_manager.player_lives]
        screen.blit(lives_surf, (20, 20))
        
def draw_score():
    score_text = font.render(f"SCORE: {game_manager.score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(topright=(GameSettings.SCREEN_WIDTH - 20, 20))
    screen.blit(score_text, score_rect)
    
def update():
    while True:
        GameSettings.dt = GameSettings.CLOCK.tick(GameSettings.FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
        game_manager.start_game()
        paddle_group.update()
        ball_group.update(brick_group)
        draw_game()
        


if __name__ == "__main__":
    brick.Brick.create_grid(brick_group, game_manager)
    update()
