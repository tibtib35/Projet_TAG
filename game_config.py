import pygame
class GameConfig:
    WINDOWH = 800
    WINDOWW = 1200
    Y_PLATFORM = 516
    PLAYER_W = 32
    PLAYER_H = 32
    PLAYER_COUNT = 2
    BACKGROUND_IMG = None
    PLAYER1_IMG = None
    PLAYER2_IMG = None
    PLAYER3_IMG = None
    DT = 0.5
    FORCE_LEFT = -20
    FORCE_RIGHT = -FORCE_LEFT
    GRAVITY = 3
    FORCE_JUMP = -60
    JUMP_DELAY = 150 # ms
    IMUNITY_TIME = 3000 # ms
    PADDING = 150
    MIN_ZOOM_W = 900       
    CAMERA_SPEED = 0.01     # 5% de déplacement vers la cible à chaque frame (plus c'est petit, plus c'est fluide)



    def init():
        GameConfig.BACKGROUND_IMG = pygame.image.load("Ressources\\background.jpg")
        player_size = (GameConfig.PLAYER_W, GameConfig.PLAYER_H)
        GameConfig.PLAYER1_IMG = pygame.transform.scale(
            pygame.image.load("Ressources\\player1.png"), player_size
        )
        GameConfig.PLAYER2_IMG = pygame.transform.scale(
            pygame.image.load("Ressources\\player2.png"), player_size
        )
        GameConfig.PLAYER3_IMG = pygame.transform.scale(
            pygame.image.load("Ressources\\player3.png"), player_size
        )