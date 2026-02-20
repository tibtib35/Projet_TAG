import pygame
from game_config import GameConfig

class Player(pygame.sprite.Sprite):
    def __init__(self, x):
        self.vx = 0
        self.vy = 0
        pygame.sprite.Sprite.__init__(self)
        self.hitbox_width = 32
        self.rect = pygame.Rect(x, GameConfig.Y_PLATFORM - GameConfig.PLAYER_H, self.hitbox_width, GameConfig.PLAYER_H)
        self.image = GameConfig.STANDING_IMG
        

    def draw(self, window):
        offset_x = (GameConfig.PLAYER_W - self.hitbox_width) // 2
        window.blit(self.image, (self.rect.x - offset_x, self.rect.y))

    # On ajoute l'argument 'obstacle'
    def advance_state(self, next_move, obstacle):
        # --- 1. Calcul des forces (inchangé) ---
        fx = 0
        fy = 0
        if next_move.left:
            fx = GameConfig.FORCE_LEFT
        elif next_move.right:
            fx = GameConfig.FORCE_RIGHT
        
        self.vx = fx * GameConfig.DT
        
        if next_move.jump:
            fy = GameConfig.FORCE_JUMP

        # Gravité et saut
        # On peut sauter si on est au sol OU si on est sur l'obstacle
        if self.on_ground() or self.on_obstacle(obstacle):
            self.vy = fy * GameConfig.DT
        else:
            self.vy = self.vy + GameConfig.GRAVITY * GameConfig.DT

        # --- 2. Application du mouvement HORIZONTAL (X) ---
        # On bouge uniquement en X d'abord
        dx = self.vx * GameConfig.DT
        self.rect = self.rect.move(dx, 0)
        
        # Vérification collision X (Murs)
        for obs in obstacle:
            if self.rect.colliderect(obs):
                if dx > 0: # On allait vers la droite
                    self.rect.right = obs.left # On se colle au bord gauche du mur
                elif dx < 0: # On allait vers la gauche
                    self.rect.left = obs.right # On se colle au bord droit du mur
                self.vx = 0

        # Limitation aux bords de l'écran (X)
        if self.rect.x < 0: 
            self.rect.x = 0
        elif self.rect.x > GameConfig.WINDOWW - self.rect.width: 
            self.rect.x = GameConfig.WINDOWW - self.rect.width
        # --- 3. Application du mouvement VERTICAL (Y) ---
        # On bouge ensuite en Y
        dy = self.vy * GameConfig.DT
        self.rect = self.rect.move(0, dy)

        # Vérification collision Y (Sol et Plafond)
        for obs in obstacle:
            if self.rect.colliderect(obs):
                if dy > 0: # On tombait vers le bas
                    self.rect.bottom = obs.top # On atterrit dessus
                    self.vy = 0 
                elif dy < 0: # On sautait vers le haut (tête cogne)
                    self.rect.top = obs.bottom # On tape le dessous
                self.vy = 0

        # Limitation au sol global (Y)
        # Note: on limite self.vy pour ne pas traverser le sol du bas trop vite
        if self.rect.bottom > GameConfig.Y_PLATFORM:
            self.rect.bottom = GameConfig.Y_PLATFORM
            self.vy = 0

    def on_ground(self):
        return self.rect.bottom >= GameConfig.Y_PLATFORM

    # Vérifie si on est posé sur l'obstacle pour pouvoir resauter
    def on_obstacle(self, obstacle):
        # On crée un petit rectangle juste sous les pieds du joueur pour tester
        test_rect = pygame.Rect(self.rect.x, self.rect.bottom, self.rect.width, 2)
        # Si ce petit rectangle touche l'obstacle, c'est qu'on est juste dessus
        for obs in obstacle:
            if test_rect.colliderect(obs):
                return True
        return False