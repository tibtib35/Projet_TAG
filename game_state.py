import pygame
from game_config import GameConfig
from player import Player

class GameState:
    def __init__(self):
        self.player = [Player(20), Player(GameConfig.WINDOWW - 20 - GameConfig.PLAYER_W)]
        self.image = GameConfig.STANDING_IMG
        self.obstacle = [pygame.Rect(500, 400, 200, 20), pygame.Rect(400, 300, 200, 20)]

    def draw(self,window):
        window.blit(GameConfig.BACKGROUND_IMG, (0, 0))
        for p in self.player:
            p.draw(window)
        for obs in self.obstacle:
            pygame.draw.rect(window, (0, 0, 0), obs)

    def advance_state(self, next_move):
        for p in self.player:
            p.advance_state(next_move, self.obstacle)

