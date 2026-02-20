import pygame
from game_config import GameConfig
from player import Player

class GameState:
    def __init__(self):
        self.player = Player(20)
        self.image = GameConfig.STANDING_IMG
        self.obstacle = pygame.Rect(230, 400, 200, 20)


    def draw(self,window):
        window.blit(GameConfig.BACKGROUND_IMG, (0, 0))
        self.player.draw(window)
        pygame.draw.rect(window, (0, 0, 0), self.obstacle)

    def advance_state(self, next_move):
        self.player.advance_state(next_move, self.obstacle)

