import pygame
from game_config import GameConfig
from player import Player

class GameState:
    def __init__(self):
        self.player = [Player(20), Player(GameConfig.WINDOWW - 20 - GameConfig.PLAYER_W)]
        self.player[0].is_it = True
        self.image = GameConfig.STANDING_IMG
        self.obstacle = [pygame.Rect(500, 400, 200, 20), pygame.Rect(400, 300, 200, 20)]

    def draw(self,window):
        window.blit(GameConfig.BACKGROUND_IMG, (0, 0))
        for p in self.player:
            p.draw(window)
        for obs in self.obstacle:
            pygame.draw.rect(window, (0, 0, 0), obs)

    def advance_state(self, all_moves):
        for i, p in enumerate(self.player):
            p.advance_state(all_moves[i], self.obstacle)

        current_time = pygame.time.get_ticks()

        loup = None
        for p in self.player:
            if p.is_it:
                loup = p
                break

        if loup:
            for p in self.player:
                # Si le loup touche quelqu'un d'autre
                if p != loup and loup.rect.colliderect(p.rect):
                    # On vérifie que le loup n'a pas été touché il y a moins d'une seconde
                    # Cela évite que le rôle ne revienne en boucle instantanément
                    if current_time - p.last_tagged_time > GameConfig.IMUNITY_TIME: 
                        loup.is_it = False
                        loup.last_tagged_time = current_time # L'ancien loup devient immunisé 1s
                        p.is_it = True
                        p.last_tagged_time = current_time # Le nouveau loup reçoit son rôle
                        break

