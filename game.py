import pygame

def game_loop(surface):
    quitting = False
    while not quitting:
        #gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitting = True
        #Affichage de la nouvelle image

        pygame.time.delay(20)
        pygame.display.update()

if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode(size=(800, 500))
    pygame.display.set_caption("Premier jeu")
    game_loop(window)
    pygame.quit()  