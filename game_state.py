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
            self.tiled_map = TiledMap("Ressources\\carte1_TAG.tmx")
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

        
        if self.tiled_map:
            map_w = self.tiled_map.width
            map_h = self.tiled_map.height
        else:
            map_w = GameConfig.WINDOWW
            map_h = GameConfig.WINDOWH

        GameConfig.MAP_W = map_w
        GameConfig.MAP_H = map_h
            
        
        self.canvas = pygame.Surface((map_w, map_h))
        self.camera_actuelle = None

    def _create_players_from_spawns(self, spawn_points):
        players = []
        spawns = [f"spawn_j{i + 1}" for i in range(max(1, GameConfig.PLAYER_COUNT))]
        for i, spawn_name in enumerate(spawns):
            if spawn_name not in spawn_points:
                continue

            spawn_x, spawn_y = spawn_points[spawn_name]
            p = Player(spawn_x, i)
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
            p = Player(x, i)
            players.append(p)

        return players

    def draw(self, window):
        # 1. On nettoie notre grande feuille avec une couleur de fond (noir)
        self.canvas.fill((0, 0, 0))

        # 2. On dessine l'image de fond (si elle existe)
        if GameConfig.BACKGROUND_IMG:
            # Attention : le fond doit maintenant faire la taille du canvas, pas de la fenêtre !
            canvas_size = self.canvas.get_size()
            if self._scaled_background is None or self._scaled_background_size != canvas_size:
                self._scaled_background = pygame.transform.scale(GameConfig.BACKGROUND_IMG, canvas_size)
                self._scaled_background_size = canvas_size
            
            # On colle le fond sur le CANVAS
            self.canvas.blit(self._scaled_background, (0, 0))
        
        # 3. On dessine la carte Tiled sur le CANVAS
        if self.tiled_map:
            self.tiled_map.draw(self.canvas)
            
        # 4. On dessine tous les joueurs sur le CANVAS
        for p in self.player:
            p.draw(self.canvas)
            
        # 5. On dessine les obstacles de secours (si la carte n'a pas chargé) sur le CANVAS
        if not self.tiled_map:
            for obs in self.obstacle:
                pygame.draw.rect(self.canvas, (0, 0, 0), obs)

        
        # On crée des listes avec les coordonnées de chaque joueur
        tous_les_x_gauche = [p.rect.left for p in self.player]
        tous_les_x_droite = [p.rect.right for p in self.player]
        tous_les_y_haut = [p.rect.top for p in self.player]
        tous_les_y_bas = [p.rect.bottom for p in self.player]

        # On prend le plus petit X/Y et le plus grand X/Y
        min_x = min(tous_les_x_gauche)
        max_x = max(tous_les_x_droite)
        min_y = min(tous_les_y_haut)
        max_y = max(tous_les_y_bas)

        
        # ajout du padding
        box_w = (max_x - min_x) + (GameConfig.PADDING * 2)
        box_h = (max_y - min_y) + (GameConfig.PADDING * 2)

        # pas de camera trop petite
        if box_w < GameConfig.MIN_ZOOM_W:
            box_w = GameConfig.MIN_ZOOM_W

        # Maintient du ratio
        ratio_ecran = GameConfig.WINDOWW / GameConfig.WINDOWH
        ratio_boite = box_w / box_h

        # Si la boîte est trop large par rapport à l'écran, on augmente sa hauteur
        if ratio_boite > ratio_ecran:
            box_h = box_w / ratio_ecran
        # Sinon, si elle est trop haute, on augmente sa largeur
        else:
            box_w = box_h * ratio_ecran

        #Créer le rectangle "CIBLE" (là où la caméra VOUDRAIT être)
        centre_x = (min_x + max_x) // 2
        centre_y = (min_y + max_y) // 2
        
        camera_cible = pygame.Rect(0, 0, int(box_w), int(box_h))
        camera_cible.center = (centre_x, centre_y)

        
        #Si c'est la toute première image du jeu, la caméra se téléporte direct sur la cible
        if self.camera_actuelle is None:
            self.camera_actuelle = camera_cible.copy()
            
        #Sinon, on rapproche la caméra actuelle de la cible en douceur
        else:
            vitesse = GameConfig.CAMERA_SPEED
            
            # On lisse la taille (le zoom)
            nouvelle_largeur = self.camera_actuelle.width + (camera_cible.width - self.camera_actuelle.width) * vitesse
            nouvelle_hauteur = self.camera_actuelle.height + (camera_cible.height - self.camera_actuelle.height) * vitesse
            
            # On lisse la position (le centre)
            nouveau_cx = self.camera_actuelle.centerx + (camera_cible.centerx - self.camera_actuelle.centerx) * vitesse
            nouveau_cy = self.camera_actuelle.centery + (camera_cible.centery - self.camera_actuelle.centery) * vitesse
            
            # On met à jour notre vraie caméra 
            self.camera_actuelle.width = int(nouvelle_largeur)
            self.camera_actuelle.height = int(nouvelle_hauteur)
            self.camera_actuelle.center = (int(nouveau_cx), int(nouveau_cy))

        rect_de_la_carte = self.canvas.get_rect()

        # Sécurité: subsurface exige un rectangle entièrement contenu
        # dans la surface source (même taille incluse).
        self.camera_actuelle.width = max(1, min(self.camera_actuelle.width, rect_de_la_carte.width))
        self.camera_actuelle.height = max(1, min(self.camera_actuelle.height, rect_de_la_carte.height))
        self.camera_actuelle.clamp_ip(rect_de_la_carte)

        
        #On découpe la zone du canvas avec notre caméra 
        vue_camera = self.canvas.subsurface(self.camera_actuelle)
        
        # On redimensionne sans déformer l'image (letterbox/pillarbox si besoin)
        src_w, src_h = vue_camera.get_size()
        dst_w, dst_h = window.get_size()
        
        scale = min(dst_w / src_w, dst_h / src_h)
        render_w = max(1, int(src_w * scale))
        render_h = max(1, int(src_h * scale))
        
        vue_finale = pygame.transform.smoothscale(vue_camera, (render_w, render_h))
        
        offset_x = (dst_w - render_w) // 2
        offset_y = (dst_h - render_h) // 2
        window.fill((0, 0, 0))
        window.blit(vue_finale, (offset_x, offset_y))

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

