import pygame
from game_config import GameConfig
from game_state import GameState
from move import Move


def update_window_size(width, height):
    GameConfig.WINDOWW = max(960, int(width))
    GameConfig.WINDOWH = max(540, int(height))
    return pygame.display.set_mode((GameConfig.WINDOWW, GameConfig.WINDOWH), pygame.RESIZABLE)

def get_next_moves(player_count):
    moves = [Move() for _ in range(player_count)]
    keys = pygame.key.get_pressed()
    for i in range(player_count):
        b = GameConfig.KEYS[i]
        if keys[b['jump']]:  moves[i].jump  = True
        if keys[b['left']]:  moves[i].left  = True
        if keys[b['right']]: moves[i].right = True
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
        button_2p.center = (GameConfig.WINDOWW // 4, GameConfig.WINDOWH // 2 + 50)
        button_3p.center = (3 * GameConfig.WINDOWW // 4, GameConfig.WINDOWH // 2 + 50)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.VIDEORESIZE:
                surface = update_window_size(event.w, event.h)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_2p.collidepoint(mouse_pos):
                    return 2
                if button_3p.collidepoint(mouse_pos):
                    return 3


        surface.fill((0, 0, 0))

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


def parametres_screen(surface):
    font_titre  = pygame.font.SysFont('Consolas', 55, bold=True)
    font_normal = pygame.font.SysFont('Consolas', 28)

    actions       = ['jump', 'left', 'right']
    labels_act    = ['SAUT', 'GAUCHE', 'DROITE']
    labels_joueur = ['JOUEUR 1', 'JOUEUR 2', 'JOUEUR 3']

    time_selection = ["30", "60", "90"]

    selected = None  # (player_idx, action_idx) en attente d'une touche
    COL_W, ROW_H = 170, 55

    

    button_retour = pygame.Rect(0, 0, 240, 55)

    while True:
        cx       = GameConfig.WINDOWW // 2
        start_x  = cx - (3 * COL_W) // 2
        start_y  = 170
        button_retour.center = (cx, GameConfig.WINDOWH - 55)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.VIDEORESIZE:
                surface = update_window_size(event.w, event.h)
            if event.type == pygame.KEYDOWN:
                if selected:
                    pi, ai = selected
                    GameConfig.KEYS[pi][actions[ai]] = event.key
                    selected = None
                elif event.key == pygame.K_ESCAPE:
                    return "RETOUR"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_retour.collidepoint(mouse_pos):
                    return "RETOUR"
                for i in range(3):
                    time_rect = pygame.Rect(start_x + i * COL_W,
                                           470,
                                           COL_W, 60)
                    if time_rect.collidepoint(mouse_pos):
                        GameConfig.GAME_TIME = int(time_selection[i])
                for pi in range(3):
                    for ai in range(3):
                        cell = pygame.Rect(start_x + ai * COL_W,
                                           start_y + (pi + 1) * ROW_H,
                                           COL_W, ROW_H)
                        if cell.collidepoint(mouse_pos):
                            selected = (pi, ai)

        surface.fill((0, 0, 0))

        titre = font_titre.render("PARAMETRES", True, (255, 215, 0))
        surface.blit(titre, (cx - titre.get_width() // 2, 80))

        # En-têtes colonnes
        for ai, lbl in enumerate(labels_act):
            t = font_normal.render(lbl, True, (180, 180, 180))
            surface.blit(t, (start_x + ai * COL_W + COL_W // 2 - t.get_width() // 2,
                             start_y + 12))

        # Grille
        for pi in range(3):
            lbl = font_normal.render(labels_joueur[pi], True, (255, 255, 255))
            surface.blit(lbl, (start_x - lbl.get_width() - 15,
                               start_y + (pi + 1) * ROW_H + ROW_H // 2 - lbl.get_height() // 2))
            for ai in range(3):
                cell = pygame.Rect(start_x + ai * COL_W,
                                   start_y + (pi + 1) * ROW_H,
                                   COL_W, ROW_H)
                is_sel = selected == (pi, ai)
                border_color = (255, 215, 0) if is_sel else (80, 80, 80)
                pygame.draw.rect(surface, border_color, cell, 2)

                key_name = "???" if is_sel else pygame.key.name(GameConfig.KEYS[pi][actions[ai]]).upper()
                color    = (255, 215, 0) if is_sel else (100, 255, 100)
                t = font_normal.render(key_name, True, color)
                surface.blit(t, (cell.centerx - t.get_width() // 2,
                                 cell.centery - t.get_height() // 2))


        if selected:
            msg = font_normal.render("Appuie sur une touche...", True, (255, 215, 0))
            surface.blit(msg, (cx - msg.get_width() // 2,
                               start_y + 4 * ROW_H + 10))
            
        t_txt = font_normal.render("time", True, (255, 255, 255))
        surface.blit(t_txt, (start_x - t_txt.get_width() - 15, 500 - t_txt.get_height() // 2))


        for i in range(3):
            time_value = int(time_selection[i])
            time_rect = pygame.Rect(start_x + i * COL_W,
                                   470,
                                   COL_W, 60)
            
            is_selected = time_value == GameConfig.GAME_TIME
            is_hovered = time_rect.collidepoint(mouse_pos)
            
            # Déterminer la couleur
            if is_selected:
                color = (100, 255, 100)
                border_color = (100, 255, 100)
            elif is_hovered:
                color = (255, 215, 0)
                border_color = (255, 215, 0)
            else:
                color = (255, 255, 255)
                border_color = (80, 80, 80)
            
            pygame.draw.rect(surface, border_color, time_rect, 2)
            
            t_lbl = font_normal.render(time_selection[i], True, color)
            surface.blit(t_lbl, (start_x + i * COL_W + COL_W // 2 - t_lbl.get_width() // 2,
                                 500 - t_lbl.get_height() // 2))

        couleur_r = (100, 255, 100) if button_retour.collidepoint(mouse_pos) else (255, 255, 255)
        txt_r = font_normal.render("RETOUR", True, couleur_r)
        surface.blit(txt_r, (button_retour.centerx - txt_r.get_width() // 2,
                              button_retour.centery - txt_r.get_height() // 2))

        pygame.display.update()


def main_menu(surface):
    font_titre = pygame.font.SysFont('Consolas', 80, bold=True)
    font_bouton = pygame.font.SysFont('Consolas', 50)

    button_jouer   = pygame.Rect(0, 0, 320, 70)
    button_params  = pygame.Rect(0, 0, 320, 70)
    button_quitter = pygame.Rect(0, 0, 320, 70)

    while True:
        button_jouer.center   = (GameConfig.WINDOWW // 2, GameConfig.WINDOWH // 2 - 60)
        button_params.center  = (GameConfig.WINDOWW // 2, GameConfig.WINDOWH // 2 + 20)
        button_quitter.center = (GameConfig.WINDOWW // 2, GameConfig.WINDOWH // 2 + 100)

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.VIDEORESIZE:
                surface = update_window_size(event.w, event.h)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_jouer.collidepoint(mouse_pos):
                    return "PLAY"
                if button_params.collidepoint(mouse_pos):
                    if parametres_screen(surface) == "QUIT":
                        return "QUIT"
                if button_quitter.collidepoint(mouse_pos):
                    return "QUIT"

        surface.fill((0, 0, 0))

        titre = font_titre.render("LOUP-TOUCHE", True, (255, 215, 0))
        surface.blit(titre, (GameConfig.WINDOWW // 2 - titre.get_width() // 2, 150))

        def blit_centre(txt_surf, rect):
            surface.blit(txt_surf, (rect.centerx - txt_surf.get_width() // 2,
                                    rect.centery - txt_surf.get_height() // 2))

        couleur_j = (100, 255, 100) if button_jouer.collidepoint(mouse_pos) else (255, 255, 255)
        blit_centre(font_bouton.render("JOUER", True, couleur_j), button_jouer)

        couleur_p = (100, 255, 100) if button_params.collidepoint(mouse_pos) else (255, 255, 255)
        blit_centre(font_bouton.render("PARAMETRES", True, couleur_p), button_params)

        couleur_q = (100, 255, 100) if button_quitter.collidepoint(mouse_pos) else (255, 255, 255)
        blit_centre(font_bouton.render("QUITTER", True, couleur_q), button_quitter)

        pygame.display.update()




def game_loop(surface):
    quitting = False
    game_state = GameState()
    clock = pygame.time.Clock()

    counter, text = GameConfig.GAME_TIME, str(GameConfig.GAME_TIME).rjust(3)
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
    
    running = True
    while running:
        # 1. Menu principal
        if main_menu(window) == "QUIT":
            break

        # 2. Sélection du nombre de joueurs
        nb_joueurs = selected_player(window)
        if nb_joueurs == "QUIT":
            break

        GameConfig.PLAYER_COUNT = nb_joueurs
        pygame.event.clear()

        # 3. Partie
        index_perdant = game_loop(window)

        # 4. Écran de fin — REPLAY relance depuis le menu principal
        if end_screen(window, index_perdant) == "QUIT":
            break

    pygame.quit()
