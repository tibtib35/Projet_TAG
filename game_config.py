import pygame
class GameConfig:
    WINDOWH = 640
    WINDOWW = 960
    Y_PLATFORM = 516
    PLAYER_W = 64
    PLAYER_H = 64
    BACKGROUND_IMG = None
    STANDING_IMG = None
    DT = 0.5
    FORCE_LEFT = -20
    FORCE_RIGHT = -FORCE_LEFT
    GRAVITY = 4
    FORCE_JUMP = -67
    JUMP_DELAY = 150 # ms
    IMUNITY_TIME = 3000 # ms



    def init():
        GameConfig.BACKGROUND_IMG = pygame.image.load("Ressources\\background.png")
        GameConfig.STANDING_IMG = pygame.image.load("Ressources\\standing.png")