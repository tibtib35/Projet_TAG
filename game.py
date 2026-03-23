import pygame
from game_config import GameConfig
from game_state import GameState
from move import Move


def update_window_size(width, height):
    GameConfig.WINDOWW = max(960, int(width))
    GameConfig.WINDOWH = max(540, int(height))
    return pygame.display.set_mode((GameConfig.WINDOWW, GameConfig.WINDOWH), pygame.RESIZABLE)

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


def selected_player(surface):
    #  Séléction des polices et de la taille des textes
    font_titre = pygame.font.SysFont('Consolas', 80, bold=True)
    font_nb_players = pygame.font.SysFont('Consolas', 50)

    # Création du rectangle pour le bouton 2 PLAYERS
    button_2p = pygame.Rect(0, 0, 250, 80)
    button_2p.center = (GameConfig.WINDOWW //4, GameConfig.WINDOWH // 2 + 50)

    # Création du rectangle pour le bouton 3 PLAYERS
    button_3p = pygame.Rect(0, 0, 250, 80)
    button_3p.center = (3 * GameConfig.WINDOWW // 4, GameConfig.WINDOWH // 2 + 50)

    waiting = True
    # On force un premier affichage propre avant d'entrer dans la boucle
    surface.fill((0, 0, 0))
    pygame.display.update()

    while waiting:
        button_rect = pygame.Rect(0, 0, 250, 80)
        button_rect.center = (GameConfig.WINDOWW // 2, GameConfig.WINDOWH // 2 + 50)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.VIDEORESIZE:
                surface = update_window_size(event.w, event.h)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_3p.collidepoint(mouse_pos) or button_2p.collidepoint(mouse_pos):
                    return "PLAY"



        # Affichage du titre
        titre_surface = font_titre.render("LOUP-TOUCHE", True, (255, 215, 0))
        surface.blit(titre_surface, (GameConfig.WINDOWW//2 - titre_surface.get_width()//2, 150))

        # Affichage du bouton 2 PLAYERS avec potentielle surbrillance
        couleur_2p = (100, 255, 100) if button_2p.collidepoint(mouse_pos) else (255, 255, 255)
        txt_2_players = font_nb_players.render("2 PLAYERS", True, couleur_2p)
        surface.blit(txt_2_players, button_2p.topleft)

        # Affichage du bouton 3 PLAYERS avec potentielle surbrillance
        couleur_3p = (100, 255, 100) if button_3p.collidepoint(mouse_pos) else (255, 255, 255)
        txt_3_players = font_nb_players.render("3 PLAYERS", True, couleur_3p)
        surface.blit(txt_3_players, button_3p.topleft)

        pygame.display.update()


def game_loop(surface):
    quitting = False
    game_state = GameState()
    clock = pygame.time.Clock()

    counter, text = 30, '30'.rjust(3)
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    font = pygame.font.SysFont('Consolas', 30)

    while not quitting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitting = True
            if event.type == pygame.VIDEORESIZE:
                surface = update_window_size(event.w, event.h)
            if event.type == pygame.USEREVENT:
                if not counter <= 0:
                    counter -= 1
                    text = str(counter).rjust(3)
                else:
                    quitting = True

        # On récupère la liste des mouvements pour tous les joueurs
        all_moves = get_next_moves(len(game_state.player))

        game_state.advance_state(all_moves)

        # Affichage
        game_state.draw(surface)

        # Affichage du timer
        timer_surface = font.render(text, True, (0, 0, 0))
        timer_rect = timer_surface.get_rect(midtop=(GameConfig.WINDOWW // 2, 20))
        surface.blit(timer_surface, timer_rect)

        pygame.display.update()
        clock.tick(60)

    pygame.time.set_timer(pygame.USEREVENT, 0)

    # Trouver le perdant (celui qui est loup quand le timer atteint 0)
    for i, p in enumerate(game_state.player):
        if p.is_it:
            return i


def end_screen(surface, index_perdant):
    # --- Polices ---
    font_titre = pygame.font.SysFont('Consolas', 80, bold=True)
    font_bouton = pygame.font.SysFont('Consolas', 50)

    # --- Création des boutons (positionnés à gauche et à droite) ---
    button_replay = pygame.Rect(0, 0, 250, 80)
    button_replay.center = (GameConfig.WINDOWW // 4, GameConfig.WINDOWH // 2 + 50)

    button_quit = pygame.Rect(0, 0, 250, 80)
    button_quit.center = (3 * GameConfig.WINDOWW // 4, GameConfig.WINDOWH // 2 + 50)

    waiting = True


    surface.fill((0, 0, 0))
    pygame.display.update()
    while waiting:
        mouse_pos = pygame.mouse.get_pos()

        # --- Gestion des événements ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.VIDEORESIZE:
                surface = update_window_size(event.w, event.h)
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Clic sur REJOUER → on retourne au menu
                if button_replay.collidepoint(mouse_pos):
                    return "REPLAY"
                # Clic sur QUITTER → on ferme le jeu
                if button_quit.collidepoint(mouse_pos):
                    return "QUIT"

        # --- Dessin ---
        # Fond noir
        surface.fill((0, 0, 0))

        # Titre : on affiche le numéro du perdant (index + 1 car index commence à 0)
        titre = font_titre.render(f"Joueur {index_perdant + 1} a perdu !", True, (255, 50, 50))
        surface.blit(titre, (GameConfig.WINDOWW // 2 - titre.get_width() // 2, 150))

        # Bouton REJOUER (vert si survolé, blanc sinon)
        couleur_replay = (100, 255, 100) if button_replay.collidepoint(mouse_pos) else (255, 255, 255)
        txt_replay = font_bouton.render("REJOUER", True, couleur_replay)
        surface.blit(txt_replay, button_replay.topleft)

        # Bouton QUITTER (vert si survolé, blanc sinon)
        couleur_quit = (100, 255, 100) if button_quit.collidepoint(mouse_pos) else (255, 255, 255)
        txt_quit = font_bouton.render("QUITTER", True, couleur_quit)
        surface.blit(txt_quit, button_quit.topleft)

        pygame.display.update()


if __name__ == "__main__":
    pygame.init()
    GameConfig.init()

    info = pygame.display.Info()
    initial_w = int(info.current_w * 0.9)
    initial_h = int(info.current_h * 0.9)
    window = update_window_size(initial_w, initial_h)

    pygame.display.set_caption("TAG")

    # On lance le menu de sélection du nombre de joueurs
    choix = selected_player(window)
    pygame.event.clear()
    # Boucle principale : on rejoue tant que le joueur le veut
    while choix == "PLAY":
        # On lance la partie et on récupère l'index du perdant
        index_perdant = game_loop(window)
        # On affiche l'écran de fin avec le nom du perdant
        choix = end_screen(window, index_perdant)
        # Si le joueur veut rejouer, on retourne au menu de sélection
        if choix == "REPLAY":
            choix = selected_player(window)

    pygame.quit()

    "batard"