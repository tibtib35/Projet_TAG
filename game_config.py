import pygame
class GameConfig:
    WINDOWH = 800
    WINDOWW = 1200
    MAP_W = 1200
    MAP_H = 800   
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
    IMUNITY_TIME = 1500 # ms
    PADDING = 150
    MIN_ZOOM_W = 900       
    CAMERA_SPEED = 0.05     # 5% de déplacement vers la cible à chaque frame (plus c'est petit, plus c'est fluide)
    STANDING_IMG = None
    BONUS_DUREE       = 5000  # ms — durée d'un boost
    BONUS_VITESSE_MULT = 1.8  # multiplicateur de vitesse
    BONUS_SAUT_MULT    = 1.6  # multiplicateur de saut
    BONUS_INTERVALLE_MIN = 6000   # ms entre deux spawns (min)
    BONUS_INTERVALLE_MAX = 12000  # ms entre deux spawns (max)
    KEYS = [
        {'jump': pygame.K_UP,   'left': pygame.K_LEFT, 'right': pygame.K_RIGHT},
        {'jump': pygame.K_z,    'left': pygame.K_q,    'right': pygame.K_d},
        {'jump': pygame.K_i,    'left': pygame.K_j,    'right': pygame.K_l},
    ]

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
        try:
            GameConfig.STANDING_IMG = pygame.transform.scale(
                pygame.image.load("Ressources\\standing.png"), player_size
            )
        except Exception:
            GameConfig.STANDING_IMG = None