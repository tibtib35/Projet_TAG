from matplotlib import text
import pygame
from game_config import GameConfig
from game_state import GameState
from move import Move

def get_next_move():
        next_move = Move()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            next_move.jump = True
        if keys[pygame.K_LEFT]:
            next_move.left = True
        if keys[pygame.K_RIGHT]:
            next_move.right = True
        return next_move

def game_loop(surface):
    quitting = False
    game_state = GameState()
    clock = pygame.time.Clock()

    timmer = pygame.time.Clock() #decompte de fin de partie
    counter, text = 10, '10'.rjust(3)
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    font = pygame.font.SysFont('Consolas', 30)

    while not quitting:
        # 1. Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitting = True
            if event.type == pygame.USEREVENT:
                if not counter <= 0:
                    counter -= 1
                    text = str(counter).rjust(3)
                else :
                    quitting = False
            
        
        # 2. Calcul de la logique (Mouvement et Collisions)
        next_move = get_next_move()
        game_state.advance_state(next_move)
        
        # 3. Affichage (On dessine l'état qui vient d'être calculé)
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