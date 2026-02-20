import pygame
from game_config import GameConfig
from game_state import GameState
from move import Move

def get_next_moves(player_count):
    # On crée une liste d'objets Move, un pour chaque joueur
    moves = [Move() for _ in range(player_count)]
    keys = pygame.key.get_pressed()

    # Joueur 1 : Flèches directionnelles
    if keys[pygame.K_UP]:
        moves[0].jump = True
    if keys[pygame.K_LEFT]:
        moves[0].left = True
    if keys[pygame.K_RIGHT]:
        moves[0].right = True

    # Joueur 2 : Z, Q, D (si un deuxième joueur existe)
    if player_count > 1:
        if keys[pygame.K_z]:
            moves[1].jump = True
        if keys[pygame.K_q]:
            moves[1].left = True
        if keys[pygame.K_d]:
            moves[1].right = True

    if player_count > 2:
        if keys[pygame.K_i]: moves[2].jump = True
        if keys[pygame.K_j]: moves[2].left = True
        if keys[pygame.K_l]: moves[2].right = True

            
    return moves
        

def game_loop(surface):
    quitting = False
    game_state = GameState()
    clock = pygame.time.Clock()
    
    while not quitting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitting = True
        
        # On récupère la liste des mouvements pour tous les joueurs
        all_moves = get_next_moves(len(game_state.player))
        
        # On fait avancer chaque joueur avec son propre mouvement
        for i in range(len(game_state.player)):
            # On passe l'obstacle pour la gestion des collisions
            game_state.player[i].advance_state(all_moves[i], game_state.obstacle)
        
        # Affichage
        game_state.draw(surface)
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    pygame.init()
    GameConfig.init()
    window = pygame.display.set_mode(size=(GameConfig.WINDOWW, GameConfig.WINDOWH))
    pygame.display.set_caption("TAG")
    game_loop(window)
    pygame.quit()