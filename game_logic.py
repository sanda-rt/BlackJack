import random
import interface
import pygame
import csv
from pathlib import Path

pygame.init()
pygame.mixer.init()
 
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
            (2, '♠', pygame.image.load('Image/spades_2.png')), (2, '♣', pygame.image.load('Image/clubs_2.png')),  (2, '♦', pygame.image.load('Image/diamonds_2.png')), (2, '♥', pygame.image.load('Image/hearts_2.png')),
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
            ('K', '♠', pygame.image.load('Image/spades_K.png')), ('K', '♣', pygame.image.load('Image/clubs_K.png')), ('K', '♦', pygame.image.load('Image/diamonds_K.png')), ('K', '♥', pygame.image.load('Image/hearts_K.png')),
            ('A', '♠', pygame.image.load('Image/spades_A.png')), ('A', '♣', pygame.image.load('Image/clubs_A.png')), ('A', '♦', pygame.image.load('Image/diamonds_A.png')), ('A', '♥', pygame.image.load('Image/hearts_A.png'))
        ]
        self.carte = list(self.c)

        self.dos = [pygame.image.load('Image/back_light.png'), pygame.image.load('Image/back_dark.png')]

    def melanger(self):
        random.shuffle(self.carte)
    
    def partager(self):
        if not self.carte:
            self.carte = list(self.c)
            self.melanger()
        return self.carte.pop()

class Jeu(Carte):
    def __init__(self):
        super().__init__()
        self.melanger()
        self.joueur = [self.partager(), self.partager()]
        self.croupier = [self.partager(), self.partager()]
        self.split_card = []
        self.mise = 0
        self.mise_split = 0
        self.nbr_c = 12
        self.maintenant = 0
        self.isCroupier: bool = False
        self.isSplit = False
        self.inSplit = False
        self.orderSplit = 1
        documents = Path.home() / "Documents"
        self.fichier = documents / "data.csv"
        try :
            self.fond, self.mise_max = self.charger()
        except (FileNotFoundError, IndexError):
            self.sauvegarder("10000", "10000")
            self.fond, self.mise_max = self.charger()
        self.taux_10 = 0
        self.taux_20 = 0
        self.taux_50 = 0
        self.taux_mise()
    
    def pointage(self, l: list):
        values = []
        for card in l:
            rank = card[0]
            if isinstance(rank, int):
                values.append(rank)
            elif rank in ('J', 'Q', 'K'):
                values.append(10)
            elif rank == 'A':
                values.append(11)
        total = sum(values)
        aces = sum(1 for c in l if c[0] == 'A')
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total
    
    def mise_disp(self, taux:int):
        return int(self.mise_max * taux)
    def taux_mise(self):
        self.taux_10 = self.mise_max * 0.1
        self.taux_20 = self.mise_max * 0.2
        self.taux_50 = self.mise_max * 0.5

    def mise_10(self):
        if  self.fond - self.taux_10 >= 0:
            self.mise += int(self.taux_10)
            self.fond -= int(self.taux_10)
    def mise_20(self):
        if self.fond - self.taux_20 >= 0 :
            self.mise += int(self.taux_20)
            self.fond -= int(self.taux_20)
    def mise_50(self):
        if self.fond - self.taux_50 >= 0:
            self.mise += int(self.taux_50)
            self.fond -= int(self.taux_50)
    def partage_carte(self, main: list):
        self.nbr_c -= 1
        main.append(self.partager())
        self.maintenant = pygame.time.get_ticks()
    
    def restaurer(self):
        self._carte = list(self.c)
        self.melanger()
        game_princ.bouttonMise_verif()
        self.joueur = [self.partager(), self.partager()]
        self.croupier = [self.partager(), self.partager()]
        self.maintenant = pygame.time.get_ticks()
        self.isCroupier = False

    def verification(self):
        if self.inSplit:
            self.orderSplit += 1
            if self.orderSplit == 3:
                self.isCroupier = True
                self.isSplit_card = True
        else: self.isCroupier = True
        self.maintenant = pygame.time.get_ticks()
    
    def doubler(self):
        if self.fond - self.mise >= 0:
            self.fond -= int(self.mise)
            self.mise *= 2
            self.isCroupier = True
            self.partage_carte(self.joueur)
            self.maintenant = pygame.time.get_ticks()
    
    def sauvegarder(self, argent:int, mise_max: int):
        with open(self.fichier, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["argent", "mise_max"])
            writer.writerow([argent, mise_max])
    def charger(self):
        with open(self.fichier, mode='r') as f:
            reader = csv.reader(f)
            next(reader)
            for ligne in reader:
                argent = int(ligne[0])
                mise_max = int(ligne[1])
                return argent,mise_max

class CardAnimator:
    def __init__(self, screen_width, screen_height, start_pos,dos_image):
        self.SCREEN_WIDTH_ANIMAT = screen_width
        self.SCREEN_HEIGHT_ANIMAT = screen_height
        self.start_pos_deck = start_pos  # Position (50, 0) dans votre code
        self.dos = dos_image # Image du dos de carte (self.game.dos[0] ou [1])

        self.is_animating = False
        self.draw_start_time = 0
        self.draw_duration = 500  # 500ms pour un mouvement lent
        self.card_to_animate = None
        self.target_pos = (0, 0)
        self.is_card_face_up = False

    def start_animation(self, card_tuple, target_pos, face_up=True):
        self.card_to_animate = card_tuple
        self.target_pos = target_pos
        self.is_card_face_up = face_up
        self.is_animating = True
        self.draw_start_time = pygame.time.get_ticks()

    def update(self):
        """Met à jour l'état de l'animation et retourne True si elle est en cours."""
        if not self.is_animating:
            return False

        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.draw_start_time

        if elapsed >= self.draw_duration:
            self.is_animating = False
            return False # Indique que l'animation est terminée

        return True # Indique que l'animation est en cours

    def draw(self, screen):
        """Dessine la carte en mouvement."""
        if not self.is_animating:
            return

        elapsed = pygame.time.get_ticks() - self.draw_start_time
        progress = elapsed / self.draw_duration
        n = 4  # Facteur de réduction de la carte

        # Interpolation linéaire
        current_x = self.start_pos_deck[0] + (self.target_pos[0] - self.start_pos_deck[0]) * progress
        current_y = self.start_pos_deck[1] + (self.target_pos[1] - self.start_pos_deck[1]) * progress

        # Image à afficher (face ou dos)
        card_image = self.card_to_animate[2] if self.is_card_face_up else self.dos

        screen.blit(pygame.transform.scale(card_image, (242 // n, 340 // n)), (current_x, current_y))

class Screen:
    def __init__(self, width: int, height: int):
        self.SCREEN_WIDTH = self.SCREEN_WIDTH_INIT = width
        self.SCREEN_HEIGHT = self.SCREEN_HEIGHT_INIT = height
        self.SCREEN = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Blackjack Classique")
        icon = pygame.image.load("Image/icone.png")
        pygame.display.set_icon(icon)

    def fullscreen(self):
        self.SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.SCREEN_WIDTH = self.SCREEN.get_width()
        self.SCREEN_HEIGHT = self.SCREEN.get_height()
        print(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
    
    def windowscreen(self):
        self.SCREEN = pygame.display.set_mode((self.SCREEN_WIDTH_INIT, self.SCREEN_HEIGHT_INIT))
        self.SCREEN_WIDTH = self.SCREEN_WIDTH_INIT
        self.SCREEN_HEIGHT = self.SCREEN_HEIGHT_INIT

class GameEngine(Screen):
    def __init__(self, width: int, height: int, screen_width: int, screen_height: int, start_pos: tuple,dos_image: int):
        super().__init__(width, height)
        self.STATE = "Menu"
        self.miser = True
        self.isblackjack = False
        self.game = Jeu()
        self.isAssurance = False
        self.assuranceAgree = False
        
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
        
        try:
            BACKGROUND_IMAGE = pygame.image.load('Image/BG_joker.png').convert()
            self.BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        except pygame.error:
            print("Attention: image introuvable, fond noir utilisé")
            self.BACKGROUND_IMAGE = None
        
        try:
            pygame.mixer.music.load("KOOL CATS by Kevin MacLeod.mp3")  # Remplace par ton fichier
            pygame.mixer.music.set_volume(0.5)           # Volume 50%
            pygame.mixer.music.play(-1)                  # Boucle infinie
        except pygame.error:
            print("Attention: musique introuvable ou format non supporté")
        
        self.buttons_menu = [
            interface.Button(pseudo_box.rect.x, BUTTON_START_Y, BUTTON_WIDTH, BUTTON_HEIGHT, "JOUER", self.jouer),
            interface.Button(pseudo_box.rect.x, BUTTON_START_Y + BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT, "PARAMÈTRES"),
            interface.Button(pseudo_box.rect.x, BUTTON_START_Y + 2 * BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT, "RÈGLES"),
            interface.Button(pseudo_box.rect.x, BUTTON_START_Y + 3 * BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT, "QUITTER", self.quitter)
        ]
    
    def assurance(self):
        self.assuranceAgree = True
        self.isAssurance = False
        if not self.game.inSplit:
            self.game.fond -= int(self.game.mise / 2)
            self.game.mise += int(self.game.mise / 2)
        elif self.game.inSplit:
            self.game.fond -= int(self.game.mise)
            self.game.mise += self.game.mise // 2
            self.game.mise_split += self.game.mise_split // 2
    def split(self):
        self.game.split_card = list([tuple(self.game.joueur.pop())])
        print(self.game.split_card)
        self.game.isSplit = False
        self.game.inSplit = True
        self.game.isSplit_card = True
        if self.assuranceAgree:
            self.game.fond -= int(self.game.mise/3)
            self.game.mise_split = self.game.mise
        else:
            self.game.fond -= int(self.game.mise)
            self.game.mise_split = self.game.mise

    def carte_joueur(self):
        if self.isAssurance:
            self.isAssurance = False
        if self.game.isSplit:
            self.game.isSplit = False
        if self.game.inSplit:
            match(self.game.orderSplit):
                    case 1: self.game.partage_carte(self.game.split_card)
                    case 2: self.game.partage_carte(self.game.joueur)
        else: self.game.partage_carte(self.game.joueur)
    
    def fullscreen(self):
        super().fullscreen()
        self.buttons_jeu = [
            interface.Button(648, self.SCREEN_HEIGHT / 1.1, 100, 50, "Tirer", self.carte_joueur),
            interface.Button(848, self.SCREEN_HEIGHT / 1.1, 120, 50, "Doubler", self.game.doubler),
            interface.Button(1060, self.SCREEN_HEIGHT / 1.1, 140, 50, "Terminer", self.game.verification)
        ]
        self.buttons_pause = [
            interface.Button(680, self.SCREEN_HEIGHT // 2, 150, 50, "Continuer", self.jouer),
            interface.Button(890, self.SCREEN_HEIGHT // 2, 150, 50, "Rejouer", self.rejouer),
            interface.Button(1140, self.SCREEN_HEIGHT // 2, 100, 50, "Menu", self.menu)
        ]
        self.buttons_jeuMise = [
            interface.Button(680, self.SCREEN_HEIGHT // 2 + 100, 120, 50, str(self.game.mise_disp(0.1)), self.game.mise_10),
            interface.Button(880, self.SCREEN_HEIGHT // 2 + 100, 120, 50, str(self.game.mise_disp(0.2)), self.game.mise_20),
            interface.Button(1080, self.SCREEN_HEIGHT // 2 + 100, 120, 50, str(self.game.mise_disp(0.5)), self.game.mise_50),
            interface.Button(1280, self.SCREEN_HEIGHT // 2 + 100, 100, 50, "TOUT", self.all),
            interface.Button(self.SCREEN_WIDTH // 2 - 150, self.SCREEN_HEIGHT // 2 + 200, 150, 50, "Terminer", self.terminer),
            interface.Button(self.SCREEN_WIDTH // 2 + 150, self.SCREEN_HEIGHT // 2 + 200, 100, 50, "Reset", self.reset)
        ]

    def jouer(self):
        if self.STATE == "Menu":
            self.STATE = "Jouer"
            self.fullscreen()
            self.miser = 1
            self.bouttonMise_verif()
        else:
            self.STATE = "Jouer"
        
    def quitter(self):
        self.STATE = "Quitter"
    def terminer(self):
        if self.game.mise == 0:
            pass
        else:
            self.miser = 0
    def reset(self):
        self.game.fond += int(self.game.mise)
        self.game.mise = 0
    def rejouer(self):
        self.STATE = "Jouer"
        self.miser = 1
        self.game.fond += int(self.game.mise)
        self.game.mise = 0
        self.game.restaurer()
    def bouttonMise_verif(self):
        if self.game.fond <= 5000:
            self.game.mise_max = 5000
            self.game.taux_mise()
        elif self.game.fond > int(1.5 * self.game.mise_max):
            if self.game.fond > 5000 and self.game.fond <= 15000:
                self.game.mise_max = 10000
                self.game.taux_mise()
            elif self.game.fond > 10000:
                self.game.mise_max += 10000
                self.game.taux_mise()
        elif self.game.fond > 5000 and self.game.fond <= int(0.5 * self.game.mise_max):
            self.game.mise_max -= 10000
        self.buttons_jeuMise = [
            interface.Button(680, self.SCREEN_HEIGHT // 2 + 100, 120, 50, str(self.game.mise_disp(0.1)), self.game.mise_10),
            interface.Button(880, self.SCREEN_HEIGHT // 2 + 100, 120, 50, str(self.game.mise_disp(0.2)), self.game.mise_20),
            interface.Button(1080, self.SCREEN_HEIGHT // 2 + 100, 120, 50, str(self.game.mise_disp(0.5)), self.game.mise_50),
            interface.Button(1280, self.SCREEN_HEIGHT // 2 + 100, 100, 50, "TOUT", self.all),
            interface.Button(self.SCREEN_WIDTH // 2 - 150, self.SCREEN_HEIGHT // 2 + 200, 150, 50, "Terminer", self.terminer),
            interface.Button(self.SCREEN_WIDTH // 2 + 150, self.SCREEN_HEIGHT // 2 + 200, 100, 50, "Reset", self.reset)
        ]
        
    def menu(self):
        self.STATE = "Menu"
        self.windowscreen()
        self.game.fond += int(self.game.mise)
        self.game.mise = 0
        self.game.sauvegarder(self.game.fond, self.game.mise_max)
        self.game.restaurer()
        
    def all(self):
        self.game.mise = self.game.fond
        self.game.fond = 0
    def tourCroupier(self):
        pointjoueur = self.game.pointage(self.game.joueur)
        pointCroupier = self.game.pointage(self.game.croupier)
        if self.game.inSplit:
            pointSplit_card = self.game.pointage(self.game.split_card)
        time = pygame.time.get_ticks()
        if not self.game.inSplit:
            if pointCroupier == pointjoueur:
                txt = TITLE_FONT.render("Partie nulle", True, WHITE)
                self.SCREEN.blit(txt, (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
                if time - self.game.maintenant >= 6000:
                    self.game.fond += int(self.game.mise)
                    self.game.mise = 0
                    self.miser = True
                    self.game.restaurer()
            elif pointCroupier > pointjoueur and pointCroupier <= 21:
                txt = TITLE_FONT.render("Perdu", True, WHITE)
                self.SCREEN.blit(txt, (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
                if time - self.game.maintenant >= 6000:
                    self.game.mise = 0
                    self.miser = True
                    self.game.restaurer()
            elif pointCroupier > 21:
                txt = TITLE_FONT.render("Victoire", True, WHITE)
                self.SCREEN.blit(txt, (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
                if time - self.game.maintenant >= 6000:
                    self.game.fond += int(2 * self.game.mise)
                    self.game.mise = 0
                    self.miser = True
                    self.game.restaurer()
            elif pointjoueur > pointCroupier and not self.isblackjack: self.game.partage_carte(self.game.croupier)
        else:
            if self.game.isSplit_card and pointSplit_card <= 21:
                if pointCroupier == pointSplit_card:
                    txt = TITLE_FONT.render("Partie nulle", True, WHITE)
                    self.SCREEN.blit(txt, (648, self.SCREEN_HEIGHT // 2))
                    if self.game.joueur != []:
                        if time - self.game.maintenant >= 6000:
                            self.game.fond += int(self.game.mise_split)
                            self.game.mise_split = 0
                            self.game.isSplit_card = False
                            self.game.maintenant = pygame.time.get_ticks()
                    else:
                        if time - self.game.maintenant >= 6000:
                            self.game.fond += int(self.game.mise_split)
                            self.game.mise_split = 0
                            self.game.isSplit_card = False
                            self.miser = True
                            self.game.restaurer()
                elif pointCroupier > pointjoueur and pointCroupier <= 21:
                    txt = TITLE_FONT.render("Perdu", True, WHITE)
                    self.SCREEN.blit(txt, (648, self.SCREEN_HEIGHT // 2))
                    if self.game.joueur != []:
                        if time - self.game.maintenant >= 6000:
                            self.game.mise_split = 0
                            self.game.isSplit_card = False
                            self.game.maintenant = pygame.time.get_ticks()
                    else:
                        if time - self.game.maintenant >= 6000:
                            self.game.mise_split = 0
                            self.game.isSplit_card = False
                            self.miser = True
                            self.game.restaurer()
                elif pointCroupier > 21:
                    txt = TITLE_FONT.render("Victoire", True, WHITE)
                    self.SCREEN.blit(txt, (648, self.SCREEN_HEIGHT // 2))
                    if self.game.joueur != []:
                        if time - self.game.maintenant >= 6000:
                            self.game.fond += int(2 * self.game.mise_split)
                            self.game.mise_split = 0
                            self.game.isSplit_card = False
                            self.game.maintenant = pygame.time.get_ticks()
                    else:
                        if time - self.game.maintenant >= 6000:
                            self.game.fond += int(2 * self.game.mise_split)
                            self.game.mise_split = 0
                            self.game.isSplit_card = False
                            self.miser = True
                            self.game.restaurer()
                elif not self.isblackjack and pointSplit_card > pointCroupier: self.game.partage_carte(self.game.croupier)
            elif pointjoueur <= 21 and self.game.joueur != []:
                if pointCroupier == pointjoueur:
                    txt = TITLE_FONT.render("Partie nulle", True, WHITE)
                    self.SCREEN.blit(txt, (1300, self.SCREEN_HEIGHT // 2))
                    if time - self.game.maintenant >= 6000:
                        self.game.fond += int(self.game.mise)
                        self.game.mise = 0
                        self.miser = 1
                        self.game.inSplit = False
                        self.game.orderSplit = 1
                        self.game.restaurer()
                elif pointCroupier > pointjoueur and pointCroupier <= 21:
                    txt = TITLE_FONT.render("Perdu", True, WHITE)
                    self.SCREEN.blit(txt, (1300, self.SCREEN_HEIGHT // 2))
                    if time - self.game.maintenant >= 6000:
                        self.game.mise = 0
                        self.miser = 1
                        self.game.inSplit = False
                        self.game.orderSplit = 1
                        self.game.restaurer()
                elif pointCroupier > 21:
                    txt = TITLE_FONT.render("Victoire", True, WHITE)
                    self.SCREEN.blit(txt, (1300, self.SCREEN_HEIGHT // 2))
                    if time - self.game.maintenant >= 6000:
                        self.game.fond += int(2 * self.game.mise)
                        self.game.mise = 0
                        self.game.inSplit = False
                        self.game.orderSplit = 1
                        self.miser = 1
                        self.game.restaurer()
                elif pointjoueur > pointCroupier and not self.isblackjack: self.game.partage_carte(self.game.croupier)
    
    def pause(self):
        self.SCREEN.fill((0, 100, 0))
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

        for button in self.buttons_menu:
            button.draw(self.SCREEN)
    
    def jeu(self):
        n = 2
        time = pygame.time.get_ticks()
        self.SCREEN.fill((0, 100, 0))
        self.SCREEN.blit(pygame.transform.scale(pygame.image.load("Image/pause1.png"), (50, 50)), self.pos_rect)
        solde = str(self.game.fond)
        txt = INPUT_FONT.render(f"Solde : {solde} Ar", True, WHITE)
        mise = INPUT_FONT.render(f"Mise : {str(self.game.mise)} Ar", True, WHITE)
        self.SCREEN.blit(txt, (50, self.SCREEN_HEIGHT // 2 + 50))
        self.SCREEN.blit(mise, (50, self.SCREEN_HEIGHT // 2 + 100))
        #interface pour la mise
        if self.miser:
            self.game.nbr_c = 8
            self.game.maintenant = pygame.time.get_ticks()
            for button in self.buttons_jeuMise:
                button.draw(self.SCREEN)
            if len(self.game.joueur) == 2 and self.game.pointage(self.game.joueur) == 21:
                    self.game.isCroupier = True
                    self.isblackjack = True
            if self.game.joueur[0][0] == self.game.joueur[1][0]:
                self.game.isSplit = True
            if self.game.croupier[0][0] == "A":
                self.isAssurance = True
        #en jeu
        else:
            point = INPUT_FONT.render(f"Point : {self.game.pointage(self.game.joueur)}", True, WHITE)
            self.SCREEN.blit(point, (50, self.SCREEN_HEIGHT // 2))

            #tour du croupier
            pointJoueur = self.game.pointage(self.game.joueur)
            if self.game.inSplit:
                pointSplit_card = self.game.pointage(self.game.split_card)
            if self.game.isCroupier:
                if self.assuranceAgree:
                    if self.game.croupier[1][0] in (10, 'Q', 'J', 'K'):
                        txt = TITLE_FONT.render("Perdu", True, WHITE)
                        self.SCREEN.blit(txt, (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
                        if time - self.game.maintenant >= 5000:
                            if self.game.inSplit:
                                self.game.fond += int(self.game.mise/3)
                                self.game.fond += int(self.game.mise_split/3)
                                self.game.mise = self.game.mise_split = 0
                            else:
                                self.game.fond += int(self.game.mise/3)
                                self.game.mise = 0
                            self.miser = 1
                            self.game.restaurer()
                    else:
                        if time -  self.game.maintenant <= 0:
                            if self.game.inSplit:
                                self.game.mise = int(self.game.mise*2/3)
                                self.game.mise_split = int(self.game.mise_split*2/3)
                            else: self.game.mise = int(self.game.mise*2/3)
                        self.tourCroupier()
                else: self.tourCroupier()

                for i in range(len(self.game.croupier)):
                    self.SCREEN.blit(pygame.transform.scale(self.game.croupier[i][2], (242//n, 340//n)), (self.SCREEN_WIDTH // 2.5 +(i * 80), 250))
            else:
                self.SCREEN.blit(pygame.transform.scale(self.game.croupier[0][2], (242//n, 340//n)), (self.SCREEN_WIDTH // 2.5, 250))
                self.SCREEN.blit(pygame.transform.scale(self.game.dos[1], (242//n, 340//n)), (self.SCREEN_WIDTH // 2.5 + 80, 250))

            
            if self.game.inSplit:
                txt = INPUT_FONT.render(f"Point : {str(self.game.pointage(self.game.split_card))}", True, WHITE)
                self.SCREEN.blit(txt, (50, self.SCREEN_HEIGHT // 2 - 50))
                split = INPUT_FONT.render(f"Mise split : {self.game.mise_split} Ar", True, WHITE)
                self.SCREEN.blit(split, (50, self.SCREEN_HEIGHT // 2 + 150))
                for i in range(len(self.game.split_card)):
                    self.SCREEN.blit(pygame.transform.scale(self.game.split_card[i][2], (242//n, 340//n)), (648 + i * 80, self.SCREEN_HEIGHT / 1.4))
                for i in range(len(self.game.joueur)):
                    self.SCREEN.blit(pygame.transform.scale(self.game.joueur[i][2], (242//n, 340//n)), (1300+i*80, self.SCREEN_HEIGHT / 1.4))
            else:
                for i in range(len(self.game.joueur)):
                    self.SCREEN.blit(pygame.transform.scale(self.game.joueur[i][2], (242//n, 340//n)), (self.SCREEN_WIDTH // 2.5 + (i * 80 ), self.SCREEN_HEIGHT / 1.4))
            for i in range(self.game.nbr_c):
                self.SCREEN.blit(pygame.transform.scale(self.game.dos[1], (242//n, 340//n)), (350 + i * 130 , 20))
            if not self.game.inSplit:
                if pointJoueur > 21:
                    txt = TITLE_FONT.render("BUSTED", True, WHITE)
                    self.SCREEN.blit(txt, (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
                    if time - self.game.maintenant >= 20000:
                        self.game.mise = 0
                        self.miser = 1
                        self.game.restaurer()
            elif self.game.inSplit:
                if pointSplit_card > 21:
                    txt = TITLE_FONT.render("BUSTED", True, WHITE)
                    self.SCREEN.blit(txt, (648, self.SCREEN_HEIGHT // 2))
                    if time - self.game.maintenant >= 6000:
                        self.game.mise_split = 0
                        self.game.orderSplit = 2
                        self.game.inSplit = []
                elif pointJoueur > 21 and pointSplit_card > 21:
                    txt = TITLE_FONT.render("BUSTED", True, WHITE)
                    self.SCREEN.blit(txt, (1300, self.SCREEN_HEIGHT // 2))
                    if time - self.game.maintenant >= 6000:
                        self.game.mise = 0
                        self.miser = 1
                        self.game.inSplit = False
                        self.game.orderSplit = 1
                        self.game.restaurer()
                elif pointSplit_card < 21 and pointJoueur > 21:
                    txt = TITLE_FONT.render("BUSTED", True, WHITE)
                    self.SCREEN.blit(txt, (1300, self.SCREEN_HEIGHT // 2))
                    if time - self.game.maintenant >= 6000:
                        self.game.joueur = []
                        self.game.mise = 0
                        self.game.isCroupier = True
                        self.game.maintenant = pygame.time.get_ticks()
            if self.isblackjack:
                blackjack_txt = TITLE_FONT.render("BlackJack", True, WHITE)
                self.SCREEN.blit(blackjack_txt, (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
                if time - self.game.maintenant >= 6000:
                    self.game.fond += int(2.5 * self.game.mise)
                    self.game.mise = 0
                    self.miser = 1
                    self.isblackjack = False
                    self.game.restaurer()


            if self.isAssurance:
                self.assurancebutton = interface.Button(1300, self.SCREEN_HEIGHT / 1.1, 160, 50, "Assurance", self.assurance)
                self.assurancebutton.draw(self.SCREEN)
            if self.game.isSplit and self.isAssurance:
                self.splitbutton = interface.Button(1560, self.SCREEN_HEIGHT / 1.1, 100, 50, "Split", self.split)
                self.splitbutton.draw(self.SCREEN)
            elif not self.isAssurance and self.game.isSplit: 
                self.splitbutton = interface.Button(1300, self.SCREEN_HEIGHT / 1.1, 100, 50, "Split", self.split)
                self.splitbutton.draw(self.SCREEN)
            for button in self.buttons_jeu:
                button.draw(self.SCREEN)

if __name__ == "__main__":
    game_princ = GameEngine(800, 600, 1920, 1080, (50, 0), 1)
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or game_princ.STATE == "Quitter":
                running = False
                game_princ.game.sauvegarder(game_princ.game.fond, game_princ.game.mise_max)
                pygame.time.delay(500)
            if game_princ.STATE == "Menu":
                for button in game_princ.buttons_menu:
                    button.handle_event(event)
            if game_princ.STATE == "Jouer":
                if game_princ.miser:
                    for button in game_princ.buttons_jeuMise:
                        button.handle_event(event)
                elif not (game_princ.isblackjack and game_princ.game.isCroupier and game_princ.game.isSplit):
                        if game_princ.isAssurance:
                            game_princ.assurancebutton.handle_event(event)
                        if game_princ.game.isSplit:
                            game_princ.splitbutton.handle_event(event)
                        for button in game_princ.buttons_jeu:
                            button.handle_event(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if game_princ.pos_rect.collidepoint(mouse_pos):
                        game_princ.STATE = "Pause"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
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