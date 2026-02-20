from matplotlib import text
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

    timmer = pygame.time.Clock() #decompte de fin de partie
    counter, text = 10, '10'.rjust(3)
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    font = pygame.font.SysFont('Consolas', 30)

    while not quitting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitting = True
            if event.type == pygame.USEREVENT:
                if not counter <= 0:
                    counter -= 1
                    text = str(counter).rjust(3)
                else :
                    quitting = False
            
        
        # On récupère la liste des mouvements pour tous les joueurs
        all_moves = get_next_moves(len(game_state.player))
        
        game_state.advance_state(all_moves)
        
        # Affichage
        game_state.draw(surface)
        
        # 4. Rafraîchissement

        #Affichage du timer
        timer_surface = font.render(text, True, (0, 0, 0))
        timer_rect = timer_surface.get_rect(midtop=(GameConfig.WINDOWW // 2, 20))
        window.blit(timer_surface, timer_rect)


        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    pygame.init()
    GameConfig.init()
    window = pygame.display.set_mode(size=(GameConfig.WINDOWW, GameConfig.WINDOWH))
    pygame.display.set_caption("TAG")
    game_loop(window)
    pygame.quit()