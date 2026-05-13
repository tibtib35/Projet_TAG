import pygame
import random
from game_config import GameConfig


class Bonus:
    TAILLE = 18  # diamètre du bonus en pixels

    def __init__(self, x, y, type_bonus):
        # On centre le bonus sur la position donnée et on le pose juste au-dessus
        self.rect = pygame.Rect(x - self.TAILLE // 2, y - self.TAILLE, self.TAILLE, self.TAILLE)
        self.type = type_bonus  # 'vitesse' ou 'saut'
        self.actif = True

    def draw(self, surface):
        if not self.actif:
            return
        # Orange = boost vitesse,  Bleu clair = boost saut
        couleur = (255, 140, 0) if self.type == 'vitesse' else (0, 180, 255)
        pygame.draw.ellipse(surface, couleur, self.rect)
        pygame.draw.ellipse(surface, (255, 255, 255), self.rect, 2)


def spawn_bonus_aleatoire(obstacle_list):
    # On choisit une plateforme aléatoire (pas le sol du bas)
    plateformes = [obs for obs in obstacle_list if obs.bottom < GameConfig.Y_PLATFORM - 20]
    if not plateformes:
        return None

    plateforme = random.choice(plateformes)
    x = random.randint(plateforme.left + 5, max(plateforme.left + 6, plateforme.right - 5))
    y = plateforme.top
    type_bonus = random.choice(['vitesse', 'saut'])
    return Bonus(x, y, type_bonus)
