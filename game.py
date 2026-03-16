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




def menu_loop(surface):
    font_titre = pygame.font.SysFont('Consolas', 80, bold=True)
    font_button = pygame.font.SysFont('Consolas', 40)
    font_nb_players = pygame.font.SysFont('Consolas', 30)
    
    # Création du bouton "JOUER"
    button_rect = pygame.Rect(0, 0, 250, 80)
    button_rect.center = (GameConfig.WINDOWW // 2, GameConfig.WINDOWH // 2 + 50)
    
    waiting = True
    while waiting:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(mouse_pos):
                    return "PLAY" # On sort du menu pour jouer
    
        # Dessin du menu
        surface.fill((50, 50, 50)) # Fond gris foncé
        surface.blit(GameConfig.STANDING_IMG, (0, 0)) 


            
        # Titre
        titre_surf = font_titre.render("LOUP-TOUCHE", True, (255, 215, 0)) # Or
        surface.blit(titre_surf, (GameConfig.WINDOWW//2 - titre_surf.get_width()//2, 150))
            
        # Bouton avec effet de survol (hover)
        couleur_bouton = (100, 255, 100) if button_rect.collidepoint(mouse_pos) else (0, 200, 0)
        pygame.draw.rect(surface, couleur_bouton, button_rect, border_radius=10)
        
        txt_jouer = font_button.render("START", True, (255, 255, 255))
        txt_2_players = font_nb_players.render("1 PLAYER", True, (255, 255, 255))
        txt_3_players = font_nb_players.render("2 PLAYERS", True, (255, 255, 255))
        surface.blit(txt_jouer, (button_rect.centerx - txt_jouer.get_width()//2, button_rect.centery - txt_jouer.get_height()//2))
        surface.blit(txt_2_players, (GameConfig.WINDOWW//4 - txt_2_players.get_width()//2, button_rect.bottom + 35))
        surface.blit(txt_3_players, (3*GameConfig.WINDOWW//4, button_rect.bottom +35))
    
            
        pygame.display.update()




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
    
    choix = menu_loop(window)
    
    if choix == "PLAY":
        game_loop(window)
        
    pygame.quit()