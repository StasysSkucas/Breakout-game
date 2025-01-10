
import random

class GameSettings:

    SCREEN_WIDTH = 960
    SCREEN_HEIGHT = 540
    FPS = 120

    @classmethod
    def initialize(cls):
        import pygame
        cls.CLOCK = pygame.time.Clock()
        cls.SCREEN = pygame.display.set_mode((cls.SCREEN_WIDTH, cls.SCREEN_HEIGHT))
        cls.dt = 0