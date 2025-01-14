import pygame

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y,  game_manager):
        super().__init__()
        self.health = 3
        self.images = {
            3: pygame.image.load("./assets/Brick3.png").convert_alpha(),
            2: pygame.image.load("./assets/Brick2.png").convert_alpha(),
            1: pygame.image.load("./assets/Brick1.png").convert_alpha()
        }
        self.image = self.images[self.health]
        self.rect = self.image.get_rect(center=(x, y))
        self.game_manager = game_manager
    
    def on_hit(self):
        self.health -= 1
        if self.health <= 0:
            self.game_manager.add_score()
            self.kill()
            self.game_manager.remove_brick()
        else:
            self.image = self.images[self.health]
            
    @staticmethod
    def create_grid(brick_group, game_manager):
        brick_image = pygame.image.load("./assets/Brick1.png").convert_alpha()
        BRICK_WIDTH = brick_image.get_width()
        BRICK_HEIGHT = brick_image.get_height()
        total_bricks = 0
        for row in range(3):  
            for col in range(11):  
                x = col * (BRICK_WIDTH + 2) + 65  
                y = row * (BRICK_HEIGHT + 2) + 100
                new_brick = Brick(x, y, game_manager)
                brick_group.add(new_brick)
                total_bricks += 1
        game_manager.set_total_bricks(total_bricks)
