import pygame
from game_config import GameConfig

class Player(pygame.sprite.Sprite):
    def __init__(self, x, player_index=0):
        self.vx = 0
        self.vy = 0
        pygame.sprite.Sprite.__init__(self)
        self.hitbox_width = 32
        self.last_jump_time = 0
        self.rect = pygame.Rect(x, GameConfig.Y_PLATFORM - GameConfig.PLAYER_H, self.hitbox_width, GameConfig.PLAYER_H)

        # Image du joueur (la même pour tous les états)
        player_images = [GameConfig.PLAYER1_IMG, GameConfig.PLAYER2_IMG, GameConfig.PLAYER3_IMG]
        self.image_course = player_images[player_index % len(player_images)]
        self.image_idle = self.image_course
        self.image = self.image_course  # pour compatibilité avec le reste du code

        self.is_it = False
        self.last_tagged_time = 0

        # Direction (pour retourner le sprite)
        self.regarde_droite = True

        # État d'animation
        self.etat = 'idle'  # 'idle', 'course', 'saut'

        # Boosts temporaires
        self.boost_vitesse = 1.0
        self.boost_vitesse_fin = 0  # timestamp pygame (ms) auquel le boost expire
        self.boost_saut = 1.0
        self.boost_saut_fin = 0

    def appliquer_bonus(self, type_bonus):
        if type_bonus == 'vitesse':
            self.boost_vitesse = GameConfig.BONUS_VITESSE_MULT
            self.boost_vitesse_fin = pygame.time.get_ticks() + GameConfig.BONUS_DUREE
        elif type_bonus == 'saut':
            self.boost_saut = GameConfig.BONUS_SAUT_MULT
            self.boost_saut_fin = pygame.time.get_ticks() + GameConfig.BONUS_DUREE

    def indicator_wolf(self, surface):
        # Losange au-dessus de la tête du loup
        diametre = 10
        espacement = 15
        cx = self.rect.centerx
        cy = self.rect.top - espacement
        pygame.draw.circle(surface, (0, 0, 0), (cx, cy), diametre // 2)

    def draw(self, window):
        offset_x = (GameConfig.PLAYER_W - self.hitbox_width) // 2

        if self.is_it:
            self.indicator_wolf(window)

        # On choisit l'image selon l'état
        if self.etat == 'idle':
            img = self.image_idle
        else:
            img = self.image_course

        # On retourne le sprite si le joueur regarde à gauche
        if not self.regarde_droite:
            img = pygame.transform.flip(img, True, False)

        window.blit(img, (self.rect.x - offset_x, self.rect.y))

    def advance_state(self, next_move, obstacle):
        # --- 0. Expiration des boosts ---
        current_time = pygame.time.get_ticks()
        if self.boost_vitesse_fin > 0 and current_time > self.boost_vitesse_fin:
            self.boost_vitesse = 1.0
            self.boost_vitesse_fin = 0
        if self.boost_saut_fin > 0 and current_time > self.boost_saut_fin:
            self.boost_saut = 1.0
            self.boost_saut_fin = 0

        # --- 1. Calcul des forces ---
        fx = 0
        fy = 0
        if next_move.left:
            fx = GameConfig.FORCE_LEFT
        elif next_move.right:
            fx = GameConfig.FORCE_RIGHT

        # On applique le boost de vitesse
        self.vx = fx * GameConfig.DT * self.boost_vitesse

        if next_move.jump:
            fy = GameConfig.FORCE_JUMP * self.boost_saut

        # Gravité et saut
        # On peut sauter si on est au sol OU si on est sur l'obstacle
        if self.on_ground() or self.on_obstacle(obstacle):
            self.vy = fy * GameConfig.DT
        else:
            self.vy = self.vy + GameConfig.GRAVITY * GameConfig.DT

        # --- 2. Application du mouvement HORIZONTAL (X) ---
        dx = self.vx * GameConfig.DT
        self.rect = self.rect.move(dx, 0)

        # Vérification collision X (Murs)
        for obs in obstacle:
            if self.rect.colliderect(obs):
                if dx > 0:  # On allait vers la droite
                    self.rect.right = obs.left
                elif dx < 0:  # On allait vers la gauche
                    self.rect.left = obs.right
                self.vx = 0

        # Limitation aux bords de la carte (X)
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > GameConfig.MAP_W - self.rect.width:
            self.rect.x = GameConfig.MAP_W - self.rect.width

        # --- 3. Application du mouvement VERTICAL (Y) ---
        dy = self.vy * GameConfig.DT
        self.rect = self.rect.move(0, dy)

        # Vérification collision Y (Sol et Plafond)
        for obs in obstacle:
            if self.rect.colliderect(obs):
                if dy > 0:  # On tombait vers le bas
                    self.rect.bottom = obs.top
                    self.vy = 0
                elif dy < 0:  # On sautait vers le haut (tête cogne)
                    self.rect.top = obs.bottom
                self.vy = 0

        # Limitation au sol global (Y)
        if self.rect.bottom > GameConfig.Y_PLATFORM:
            self.rect.bottom = GameConfig.Y_PLATFORM
            self.vy = 0

        # --- 4. Mise à jour direction et état d'animation ---
        if next_move.right:
            self.regarde_droite = True
        elif next_move.left:
            self.regarde_droite = False

        if not (self.on_ground() or self.on_obstacle(obstacle)):
            self.etat = 'saut'
        elif next_move.left or next_move.right:
            self.etat = 'course'
        else:
            self.etat = 'idle'

    def on_ground(self):
        return self.rect.bottom >= GameConfig.Y_PLATFORM

    # Vérifie si on est posé sur l'obstacle pour pouvoir resauter
    def on_obstacle(self, obstacle):
        # On crée un petit rectangle juste sous les pieds du joueur pour tester
        test_rect = pygame.Rect(self.rect.x, self.rect.bottom, self.rect.width, 2)
        for obs in obstacle:
            if test_rect.colliderect(obs):
                return True
        return False
