from game_logic import GameEngine
import pygame

game_princ = GameEngine()
    
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or game_princ.STATE == "Quitter":
            running = False
            game_princ.game.sauvegarder(game_princ.game.nom, game_princ.game.fond)
            pygame.time.delay(1000)
        if game_princ.STATE == "Menu":
            for button in game_princ.buttons_menu:
                button.handle_event(event)
        if game_princ.STATE == "Jouer":
            if game_princ.miser == 1:
                for button in game_princ.buttons_jeuMise:
                    button.handle_event(event)
            else:
                for button in game_princ.buttons_jeu:
                    button.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if game_princ.pos_rect.collidepoint(mouse_pos):
                    game_princ.STATE = "Pause"
        if game_princ.STATE == "Pause":
            for button in game_princ.buttons_pause:
                button.handle_event(event)
                
        
    if game_princ.STATE == "Menu":
        game_princ.accueil()
    elif game_princ.STATE == "Jouer":
        game_princ.jeu()
    elif game_princ.STATE == "Pause":
        game_princ.pause()
        
    pygame.display.flip()
    clock.tick(30)

pygame.quit()