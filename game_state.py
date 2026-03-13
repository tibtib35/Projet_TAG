import pygame
from game_config import GameConfig
from player import Player
from tiled_map import TiledMap

class GameState:
    def __init__(self):
        self.tiled_map = None
        self._scaled_background = None
        self._scaled_background_size = None

        try:
            self.tiled_map = TiledMap("Ressources\\carte_TAG.tmx")
            GameConfig.WINDOWW = self.tiled_map.width
            GameConfig.WINDOWH = self.tiled_map.height
            GameConfig.Y_PLATFORM = self.tiled_map.height
        except Exception:
            self.tiled_map = None

        if self.tiled_map:
            self.obstacle = self.tiled_map.get_collision_rects("collisions")
            spawn_points = self.tiled_map.get_spawns("spawns")
            self.player = self._create_players_from_spawns(spawn_points)
        else:
            self.obstacle = [pygame.Rect(0, GameConfig.WINDOWH - 20, GameConfig.WINDOWW, 20)]
            self.player = self._create_default_players()

        if not self.obstacle:
            self.obstacle = [pygame.Rect(0, GameConfig.WINDOWH - 20, GameConfig.WINDOWW, 20)]

        if self.player:
            self.player[0].is_it = True

    def _create_players_from_spawns(self, spawn_points):
        players = []
        spawns = [f"spawn_j{i + 1}" for i in range(max(1, GameConfig.PLAYER_COUNT))]
        for spawn_name in spawns:
            if spawn_name not in spawn_points:
                continue

            spawn_x, spawn_y = spawn_points[spawn_name]
            p = Player(spawn_x)
            p.rect.x = spawn_x
            p.rect.y = max(0, spawn_y - GameConfig.PLAYER_H)
            players.append(p)

        if players:
            return players

        return self._create_default_players()

    def _create_default_players(self):
        count = max(1, GameConfig.PLAYER_COUNT)
        players = []

        for i in range(count):
            x = int((i + 1) * GameConfig.WINDOWW / (count + 1)) - (GameConfig.PLAYER_W // 2)
            p = Player(x)
            players.append(p)

        return players

    def draw(self,window):
        if GameConfig.BACKGROUND_IMG:
            current_size = window.get_size()
            if self._scaled_background is None or self._scaled_background_size != current_size:
                self._scaled_background = pygame.transform.scale(GameConfig.BACKGROUND_IMG, current_size)
                self._scaled_background_size = current_size
            window.blit(self._scaled_background, (0, 0))
        if self.tiled_map:
            self.tiled_map.draw(window)
        for p in self.player:
            p.draw(window)
        if not self.tiled_map:
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

