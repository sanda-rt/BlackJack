import random
import interface
import pygame
import csv
from pathlib import Path
 
TITLE_FONT = pygame.font.Font(None, 100)
BUTTON_FONT = pygame.font.Font(None, 40)
INPUT_FONT = pygame.font.Font(None, 35)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (50, 50, 50)
LIGHT_BEIGE = (210, 180, 140)
DARK_BEIGE = (180, 150, 110)
GREEN_TABLE = (0, 128, 0)
 
class Carte:
    def __init__(self):
        self.c = [
            (2, '♠', pygame.image.load('Image/spades_2.png')), (2, '♣', pygame.image.load('Image/clubs_2.png')),  (2, '♦', pygame.image.load('Image/diamonds_2.png')), (2, '♥', pygame.image.load('Image/diamonds_2.png')),
            (3, '♠', pygame.image.load('Image/spades_3.png')), (3, '♣', pygame.image.load('Image/clubs_3.png')), (3, '♦', pygame.image.load('Image/diamonds_3.png')), (3, '♥', pygame.image.load('Image/hearts_3.png')),
            (4, '♠', pygame.image.load('Image/spades_4.png')), (4, '♣', pygame.image.load('Image/clubs_4.png')), (4, '♦', pygame.image.load('Image/diamonds_4.png')), (4, '♥', pygame.image.load('Image/hearts_4.png')),
            (5, '♠', pygame.image.load('Image/spades_5.png')), (5, '♣', pygame.image.load('Image/clubs_5.png')), (5, '♦', pygame.image.load('Image/diamonds_5.png')), (5, '♥', pygame.image.load('Image/hearts_5.png')),
            (6, '♠', pygame.image.load('Image/spades_6.png')), (6, '♣', pygame.image.load('Image/clubs_6.png')), (6, '♦', pygame.image.load('Image/diamonds_6.png')), (6, '♥', pygame.image.load('Image/hearts_6.png')),
            (7, '♠', pygame.image.load('Image/spades_7.png')), (7, '♣', pygame.image.load('Image/clubs_7.png')), (7, '♦', pygame.image.load('Image/diamonds_7.png')), (7, '♥', pygame.image.load('Image/hearts_7.png')),
            (8, '♠', pygame.image.load('Image/spades_8.png')), (8, '♣', pygame.image.load('Image/clubs_8.png')), (8, '♦', pygame.image.load('Image/diamonds_8.png')), (8, '♥', pygame.image.load('Image/hearts_8.png')),
            (9, '♠', pygame.image.load('Image/spades_9.png')), (9, '♣', pygame.image.load('Image/clubs_9.png')), (9, '♦', pygame.image.load('Image/diamonds_9.png')), (9, '♥', pygame.image.load('Image/hearts_9.png')),
            (10, '♠', pygame.image.load('Image/spades_10.png')), (10, '♣', pygame.image.load('Image/clubs_10.png')), (10, '♦', pygame.image.load('Image/diamonds_10.png')), (10, '♥', pygame.image.load('Image/hearts_10.png')),
            ('J', '♠', pygame.image.load('Image/spades_J.png')), ('J', '♣', pygame.image.load('Image/clubs_J.png')), ('J', '♦', pygame.image.load('Image/diamonds_J.png')), ('J', '♥', pygame.image.load('Image/hearts_J.png')),
            ('Q', '♠', pygame.image.load('Image/spades_Q.png')), ('Q', '♣', pygame.image.load('Image/clubs_Q.png')), ('Q', '♦', pygame.image.load('Image/diamonds_Q.png')), ('Q', '♥', pygame.image.load('Image/hearts_Q.png')),
            ('K', '♠', pygame.image.load('Image/spades_K.png')), ('K', '♣', pygame.image.load('Image/clubs_K.png')), ('K', '♦', pygame.image.load('Image/diamonds_K.png')), ('K', '♥', pygame.image.load('Image/hearts_Q.png')),
            ('A', '♠', pygame.image.load('Image/spades_A.png')), ('A', '♣', pygame.image.load('Image/clubs_A.png')), ('A', '♦', pygame.image.load('Image/diamonds_A.png')), ('A', '♥', pygame.image.load('Image/hearts_A.png'))
        ]
        self._carte = list(self.c)

        self.dos = [pygame.image.load('Image/back_light.png'), pygame.image.load('Image/back_dark.png')]
    
    @property
    def carte(self):
        return self._carte

    def melanger(self):
        return random.shuffle(self.carte)
    
    def partager(self):
        return self.carte.pop()
    
    def restaurer(self):
        self._carte = list(self.c)

class Jeu(Carte):
    def __init__(self):
        super().__init__()
        self.melanger()
        self.joueur = [self.partager(), self.partager()]
        self.croupier = [self.partager(), self.partager()]
        self.mise = 0
        documents = Path.home() / "Documents"
        self.fichier = documents / "data.csv"
        try :
            self.nom, self.fond = self.charger()
        except FileNotFoundError:
            self.sauvegarder("", "10000")
        self.taux_10 = 0
        self.taux_20 = 0
        self.taux_50 = 0
        self.taux_mise()
    
    def pointage(self, l: list):
        point = {
            "K": 10, 
            "Q": 10,
            "J": 10
        }
        p = 0
        for i in range(len(l)):
            if l[i][0] == "A":
                if i+1 < len(l):
                    if l[i+1][0] in point and p + point[l[i+1][0]]+11 > 21:
                        p += 1
                    elif l[i+1][0] not in point and l[i+1][0] != "A" and  p + l[i+1][0] + 11 > 21:
                        p += 1
                    else: p += 11
                else: p += 1 if p + 11 > 21 else 11
            elif l[i][0] in point:
                p += point[l[i][0]]
            else:
                p += l[i][0]
        return p
    def mise_disp(self, taux:int):
        return int(self.fond * taux)
    def taux_mise(self):
        self.taux_10 = self.fond * 0.1
        self.taux_20 = self.fond * 0.2
        self.taux_50 = self.fond * 0.5

    def mise_10(self):
        if  self.fond - self.taux_10 >= 0:
            self.mise += self.taux_10
            self.fond -= int(self.taux_10)
    def mise_20(self):
        if self.fond - self.taux_20 >= 0 :
            self.mise += self.taux_20
            self.fond -= int(self.taux_20)
    def mise_50(self):
        if self.fond - self.taux_50 >= 0:
            self.mise += self.taux_50
            self.fond -= int(self.taux_50)
    def carte_joueur(self):
        self.joueur.append(self.partager())
    
    def verification(self, c: list, j: list):
        pass
    
    def sauvegarder(self, nom: str, argent:int):
        with open(self.fichier, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["nom", "argent"])
            writer.writerow([nom, argent])
    def charger(self):
        with open(self.fichier, mode='r') as f:
            reader = csv.reader(f)
            next(reader)
            for ligne in reader:
                nom = ligne[0]
                argent = int(ligne[1])
                return nom, argent

class GameEngine:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.STATE = "Menu"

        self.miser = 1
        
        self.game = Jeu()
        
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.SCREEN = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        
        pygame.display.set_caption("Blackjack Classique")
        icon = pygame.image.load("Image/icone.png")
        pygame.display.set_icon(icon)
        
        self.pos_rect = pygame.Rect(0, 0, 50, 50)
        
        PADDING = 20
        BUTTON_WIDTH = 250
        BUTTON_HEIGHT = 60
        BUTTON_START_Y = 250
        BUTTON_SPACING = BUTTON_HEIGHT + PADDING
        
        pseudo_box = interface.TextBox(
            self.SCREEN_WIDTH - BUTTON_WIDTH - 50,
            BUTTON_START_Y - 70,
            BUTTON_WIDTH,
            BUTTON_HEIGHT - 10,
            placeholder="Ton pseudo..."
        )
        self.buttons_menu = [
            interface.Button(pseudo_box.rect.x, BUTTON_START_Y, BUTTON_WIDTH, BUTTON_HEIGHT, "JOUER", self.jouer),
            interface.Button(pseudo_box.rect.x, BUTTON_START_Y + BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT, "PARAMÈTRES"),
            interface.Button(pseudo_box.rect.x, BUTTON_START_Y + 2 * BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT, "RÈGLES"),
            interface.Button(pseudo_box.rect.x, BUTTON_START_Y + 3 * BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT, "QUITTER", self.quitter)
        ]
        
        try:
            BACKGROUND_IMAGE = pygame.image.load('Image/BG_joker.png').convert()
            self.BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        except pygame.error:
            print("Attention: image introuvable, fond noir utilisé")
            self.BACKGROUND_IMAGE = None
        
        try:
            pygame.mixer.music.load("KOOL CATS by Kevin MacLeod.mp3")  # Remplace par ton fichier
            pygame.mixer.music.set_volume(0.2)           # Volume 50%
            pygame.mixer.music.play(-1)                  # Boucle infinie
        except pygame.error:
            print("Attention: musique introuvable ou format non supporté")
        
        self.buttons_jeu = [
            interface.Button(100, self.SCREEN_HEIGHT / 1.2, 100, 50, "Tirer", self.game.carte_joueur),
            interface.Button(270, self.SCREEN_HEIGHT / 1.2, 120, 50, "Doubler"),
            interface.Button(490, self.SCREEN_HEIGHT / 1.2, 140, 50, "Terminer", self.game.verification)
        ]
        self.buttons_pause = [
            interface.Button(20, self.SCREEN_HEIGHT // 2, 150, 50, "Continuer", self.jouer),
            interface.Button(self.SCREEN_WIDTH // 2 - 100, self.SCREEN_HEIGHT // 2, 150, 50, "Rejouer", self.rejouer),
            interface.Button(self.SCREEN_WIDTH - 150, self.SCREEN_HEIGHT // 2, 100, 50, "Menu", self.menu)
        ]
        self.buttons_jeuMise = [
            interface.Button(self.SCREEN_WIDTH // 2 - 280, self.SCREEN_HEIGHT // 2 + 100, 100, 50, str(self.game.mise_disp(0.1)), self.game.mise_10),
            interface.Button(self.SCREEN_WIDTH // 2 - 80, self.SCREEN_HEIGHT // 2 + 100, 100, 50, str(self.game.mise_disp(0.2)), self.game.mise_20),
            interface.Button(self.SCREEN_WIDTH - 280, self.SCREEN_HEIGHT // 2 + 100, 100, 50, str(self.game.mise_disp(0.5)), self.game.mise_50),
            interface.Button(self.SCREEN_WIDTH // 2 - 110, self.SCREEN_HEIGHT // 2 + 160, 150, 50, "Terminer", self.terminer)
        ]
        
    def jouer(self):
        self.STATE = "Jouer"
        self.miser = 1
    def quitter(self):
        self.STATE = "Quitter"
    def terminer(self):
        if self.game.mise == 0:
            pass
        else:
            self.miser = 0
    def rejouer(self):
        self.STATE = "Jouer"
        self.miser = 1
        self.game.fond += int(self.game.mise)
        self.game.mise = 0
        self.game.restaurer()
        self.game.melanger()
        self.game.joueur = [self.game.partager(), self.game.partager()]
        self.game.croupier = [self.game.partager(), self.game.partager()]
    def menu(self):
        self.STATE = "Menu"
        self.game.fond += int(self.game.mise)
        self.game.mise = 0
        self.game.sauvegarder(self.game.nom, self.game.fond)
        self.game.restaurer()
        self.game.melanger()
        self.game.joueur = [self.game.partager(), self.game.partager()]
        self.game.croupier = [self.game.partager(), self.game.partager()]
    
    def pause(self):
        self.SCREEN.fill((0, 0, 0))
        for button in self.buttons_pause:
            button.draw(self.SCREEN)

        
    def accueil(self):
        if self.BACKGROUND_IMAGE:
            self.SCREEN.blit(self.BACKGROUND_IMAGE, (0, 0))
        else:
            self.SCREEN.fill(BLACK)
            
        overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.SCREEN.blit(overlay, (0, 0))
        
        title_surf_1 = TITLE_FONT.render("BLACKJACK", True, LIGHT_BEIGE)
        title_surf_2 = TITLE_FONT.render("21", True, WHITE)
        self.SCREEN.blit(title_surf_1, (50, 150))
        self.SCREEN.blit(title_surf_2, (50, 250))

        #pseudo_box.draw(SCREEN)

        for button in self.buttons_menu:
            button.draw(self.SCREEN)
    
    def jeu(self):
        n = 3
        self.SCREEN.fill((0, 100, 0))
        self.SCREEN.blit(pygame.transform.scale(pygame.image.load("Image/pause1.png"), (50, 50)), self.pos_rect)
        solde = str(self.game.fond)
        txt = INPUT_FONT.render("Solde : ", True, WHITE)
        aff_solde = INPUT_FONT.render(solde, True, WHITE)
        self.SCREEN.blit(txt, (0, self.SCREEN_HEIGHT // 2 + 50))
        self.SCREEN.blit(aff_solde, (100, self.SCREEN_HEIGHT // 2 + 50))
        #print(self.miser)
        
        if self.miser == 1:
            for button in self.buttons_jeuMise:
                button.draw(self.SCREEN)
        else:
            point_joueur = str(self.game.pointage(self.game.joueur))
            point = INPUT_FONT.render("Point : ", True, WHITE)
            point_nbr = INPUT_FONT.render(point_joueur, True, WHITE)
            self.SCREEN.blit(point, (0, self.SCREEN_HEIGHT // 2))
            self.SCREEN.blit(point_nbr, (100, self.SCREEN_HEIGHT // 2))

            self.SCREEN.blit(pygame.transform.scale(self.game.croupier[0][2], (242//n, 340//n)), (self.SCREEN_WIDTH // 3, 50))
            self.SCREEN.blit(pygame.transform.scale(self.game.dos[1], (242//n, 340//n)), (self.SCREEN_WIDTH // 3 + 90, 50))
            for i in range(0, len(self.game.joueur)):
                self.SCREEN.blit(pygame.transform.scale(self.game.joueur[i][2], (242//n, 340//n)), (self.SCREEN_WIDTH // 3 + (i * 90 ), self.SCREEN_HEIGHT / 1.7))
            
            for button in self.buttons_jeu:
                button.draw(self.SCREEN)

if __name__ == "__main__":
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