import interface
import pygame
import csv
import random
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
        # Correction pour le 2 de cœur qui charge l'image du 2 de carreau
        self.c = [
            (2, '♠', pygame.image.load('Image/spades_2.png')), (2,'♣', pygame.image.load('Image/clubs_2.png')),  (2, '♦',pygame.image.load('Image/diamonds_2.png')), (2, '♥',pygame.image.load('Image/hearts_2.png')), # CORRIGÉ
            (3, '♠', pygame.image.load('Image/spades_3.png')), (3,'♣', pygame.image.load('Image/clubs_3.png')), (3, '♦',pygame.image.load('Image/diamonds_3.png')), (3, '♥',pygame.image.load('Image/hearts_3.png')),
            (4, '♠', pygame.image.load('Image/spades_4.png')), (4,'♣', pygame.image.load('Image/clubs_4.png')), (4, '♦',pygame.image.load('Image/diamonds_4.png')), (4, '♥',pygame.image.load('Image/hearts_4.png')),
            (5, '♠', pygame.image.load('Image/spades_5.png')), (5,'♣', pygame.image.load('Image/clubs_5.png')), (5, '♦',pygame.image.load('Image/diamonds_5.png')), (5, '♥',pygame.image.load('Image/hearts_5.png')),
            (6, '♠', pygame.image.load('Image/spades_6.png')), (6,'♣', pygame.image.load('Image/clubs_6.png')), (6, '♦',pygame.image.load('Image/diamonds_6.png')), (6, '♥',pygame.image.load('Image/hearts_6.png')),
            (7, '♠', pygame.image.load('Image/spades_7.png')), (7,'♣', pygame.image.load('Image/clubs_7.png')), (7, '♦',pygame.image.load('Image/diamonds_7.png')), (7, '♥',pygame.image.load('Image/hearts_7.png')),
            (8, '♠', pygame.image.load('Image/spades_8.png')), (8,'♣', pygame.image.load('Image/clubs_8.png')), (8, '♦',pygame.image.load('Image/diamonds_8.png')), (8, '♥',pygame.image.load('Image/hearts_8.png')),
            (9, '♠', pygame.image.load('Image/spades_9.png')), (9,'♣', pygame.image.load('Image/clubs_9.png')), (9, '♦',pygame.image.load('Image/diamonds_9.png')), (9, '♥',pygame.image.load('Image/hearts_9.png')),
            (10, '♠', pygame.image.load('Image/spades_10.png')), (10,'♣', pygame.image.load('Image/clubs_10.png')), (10, '♦',pygame.image.load('Image/diamonds_10.png')), (10, '♥',pygame.image.load('Image/hearts_10.png')),
            ('J', '♠', pygame.image.load('Image/spades_J.png')), ('J','♣', pygame.image.load('Image/clubs_J.png')), ('J', '♦',pygame.image.load('Image/diamonds_J.png')), ('J', '♥',pygame.image.load('Image/hearts_J.png')),
            ('Q', '♠', pygame.image.load('Image/spades_Q.png')), ('Q','♣', pygame.image.load('Image/clubs_Q.png')), ('Q', '♦',pygame.image.load('Image/diamonds_Q.png')), ('Q', '♥',pygame.image.load('Image/hearts_Q.png')),
            ('K', '♠', pygame.image.load('Image/spades_K.png')), ('K','♣', pygame.image.load('Image/clubs_K.png')), ('K', '♦',pygame.image.load('Image/diamonds_K.png')), ('K', '♥',pygame.image.load('Image/hearts_K.png')), # CORRIGÉ
            ('A', '♠', pygame.image.load('Image/spades_A.png')), ('A','♣', pygame.image.load('Image/clubs_A.png')), ('A', '♦',pygame.image.load('Image/diamonds_A.png')), ('A', '♥',pygame.image.load('Image/hearts_A.png'))
        ]
        self._carte = list(self.c)

        self.dos = [pygame.image.load('Image/back_light.png'), pygame.image.load('Image/back_dark.png')]

    @property
    def carte(self):
        return self._carte

    def melanger(self):
        random.shuffle(self.carte)
        return None

    def partager(self):
        # Vérifiez que la liste n'est pas vide avant de pop
        if self.carte:
            return self.carte.pop()
        return None # Retourne None si le paquet est vide

class Jeu(Carte):
    def __init__(self):
        super().__init__()
        self.melanger()
        # Le tirage initial doit se faire dans le Jeu.restaurer car c'est la logique de la partie
        self.joueur = []
        self.croupier = []
        self.mise = 0
        self.nbr_c = 10
        self.maintenant = 0
        self.isCroupier = 0
        documents = Path.home() / "Documents"
        self.fichier = documents / "data.csv"
        try :
            self.nom, self.fond = self.charger()
        except FileNotFoundError:
            self.sauvegarder("Tsiry", "10000")
            self.nom, self.fond = self.charger() # Recharger après sauvegarde
        self.fond = int(self.fond) # S'assurer que fond est un int
        self.taux_10 = 0
        self.taux_20 = 0
        self.taux_50 = 0
        self.taux_mise()
        self.restaurer() # Tirage initial des cartes

    def pointage(self, l: list):
        point = {
            "K": 10,
            "Q": 10,
            "J": 10
        }
        p = 0
        as_count = 0

        # Calculer d'abord la valeur des cartes sans les As
        for val, _, _ in l:
            if val == "A":
                as_count += 1
            elif val in point:
                p += point[val]
            else:
                p += val

        # Ajouter les As
        for _ in range(as_count):
            if p + 11 <= 21:
                p += 11
            else:
                p += 1
        return p

    def mise_disp(self, taux:int):
        return int(self.fond * taux)
    def taux_mise(self):
        self.taux_10 = int(self.fond * 0.1)
        self.taux_20 = int(self.fond * 0.2)
        self.taux_50 = int(self.fond * 0.5)

    def mise_10(self):
        if  self.fond - self.taux_10 >= 0:
            self.mise += self.taux_10
            self.fond -= self.taux_10
    def mise_20(self):
        if self.fond - self.taux_20 >= 0 :
            self.mise += self.taux_20
            self.fond -= self.taux_20
    def mise_50(self):
        if self.fond - self.taux_50 >= 0:
            self.mise += self.taux_50
            self.fond -= self.taux_50

    # Ces méthodes ne sont plus utilisées directement par les boutons mais par animate_draw
    def carte_joueur(self):
        # C'est la fonction qui retire la carte du paquet, mais le tirage effectif doit être fait dans animate_draw
        pass # La logique est déplacée dans GameEngine.animate_draw
    def carte_croupier(self):
        # C'est la fonction qui retire la carte du paquet, mais le tirage effectif doit être fait dans animate_draw
        pass # La logique est déplacée dans GameEngine.animate_draw

    def restaurer(self):
        self._carte = list(self.c)
        self.melanger()

        # Tirage des cartes initiales (2 pour chaque)
        self.joueur = [self.partager(), self.partager()]
        self.croupier = [self.partager(), self.partager()]
        self.nbr_c = len(self.carte) # Le nombre de cartes restantes

        self.maintenant = pygame.time.get_ticks()
        self.isCroupier = 0

    def verification(self):
        self.isCroupier = 1
        self.maintenant = pygame.time.get_ticks()

    def sauvegarder(self, nom: str, argent:int):
        # Convertir l'argent en chaîne pour le CSV
        argent_str = str(int(argent))
        with open(self.fichier, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["nom", "argent"])
            writer.writerow([nom, argent_str]) # Assurez-vous que c'est une chaîne
    def charger(self):
        with open(self.fichier, mode='r') as f:
            reader = csv.reader(f)
            next(reader)
            for ligne in reader:
                nom = ligne[0]
                argent = int(ligne[1]) # Convertir en int lors du chargement
                return nom, argent

class GameEngine:
    def __init__(self):

        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.SCREEN = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.game = Jeu()

        self.animator = CardAnimator(
            self.SCREEN_WIDTH,
            self.SCREEN_HEIGHT,
            (50, 0),
            self.game.dos[1])

        pygame.init()
        pygame.mixer.init()

        self.STATE = "Menu"

        self.miser = 1

        self.isblackjack = 0

        # self.game = Jeu() - L'objet jeu est déjà créé plus haut, on le garde

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
            pygame.mixer.music.load("KOOL CATS by Kevin MacLeod.mp3") # Remplace par ton fichier
            pygame.mixer.music.set_volume(0.2)           # Volume 50%
            pygame.mixer.music.play(-1)                  # Boucle infinie
        except pygame.error:
            print("Attention: musique introuvable ou format non supporté")

        # MISE À JOUR : Utiliser animate_draw pour le bouton Tirer
        self.buttons_jeu = [
            interface.Button(100, self.SCREEN_HEIGHT / 1.2, 100, 50, "Tirer", lambda: self.animate_draw(is_croupier=False)),
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
            interface.Button(self.SCREEN_WIDTH // 2 - 150, self.SCREEN_HEIGHT // 2 + 160, 150, 50, "Terminer", self.terminer),
            interface.Button(self.SCREEN_WIDTH // 2 + 20, self.SCREEN_HEIGHT // 2 + 160, 100, 50, "Reset", self.reset)
        ]

    def jouer(self):
        self.STATE = "Jouer"
        self.miser = 1
        self.game.taux_mise()

    def quitter(self):
        self.STATE = "Quitter"

    def terminer(self):
        if self.game.mise == 0:
            pass
        else:
            self.miser = 0
            self.game.restaurer()

    def reset(self):
        self.game.fond += self.game.mise
        self.game.mise = 0

    def rejouer(self):
        self.STATE = "Jouer"
        self.miser = 1
        self.game.fond += self.game.mise
        self.game.mise = 0
        self.game.restaurer()

    def menu(self):
        self.STATE = "Menu"
        self.game.fond += self.game.mise
        self.game.mise = 0
        self.game.sauvegarder(self.game.nom, self.game.fond)
        self.game.restaurer()


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

        #pseudo_box.draw(SCREEN)

        for button in self.buttons_menu:
            button.draw(self.SCREEN)

    # NOUVELLE MÉTHODE pour dessiner l'état du jeu sans l'animation
    def dessiner_jeu_statique(self, time):
        """Dessine l'état du jeu (mains, scores, boutons) sans l'animation."""
        n = 4
        self.SCREEN.fill((0, 100, 0))

        # self.SCREEN.blit(pygame.transform.scale(pygame.image.load("Image/pause 1.png"), (50, 50)), self.pos_rect)

        solde = str(self.game.fond)
        txt = INPUT_FONT.render("Solde : ", True, WHITE)
        aff_solde = INPUT_FONT.render(solde, True, WHITE)
        self.SCREEN.blit(txt, (0, self.SCREEN_HEIGHT // 2 + 50))
        self.SCREEN.blit(aff_solde, (100, self.SCREEN_HEIGHT // 2 + 50))

        # interface pour la mise
        if self.miser == 1:
            self.game.nbr_c = len(self.game.carte)
            self.game.taux_mise() # Mise à jour des valeurs des boutons de mise
            for i, button in enumerate(self.buttons_jeuMise):
                 # Mettre à jour le texte des boutons de mise à chaque frame
                if i == 0: button.text = str(self.game.taux_10)
                if i == 1: button.text = str(self.game.taux_20)
                if i == 2: button.text = str(self.game.taux_50)
                button.draw(self.SCREEN)

            # Logique Blackjack initial
            if len(self.game.joueur) == 2 and self.game.pointage(self.game.joueur) == 21:
                    self.game.isCroupier = 1
                    if self.game.pointage(self.game.croupier) != 21:
                        self.isblackjack = 1
        # en jeu
        else:
            point_joueur = str(self.game.pointage(self.game.joueur))
            point = INPUT_FONT.render("Point : ", True, WHITE)
            point_nbr = INPUT_FONT.render(point_joueur, True, WHITE)
            self.SCREEN.blit(point, (0, self.SCREEN_HEIGHT // 2))
            self.SCREEN.blit(point_nbr, (100, self.SCREEN_HEIGHT // 2))

            # tour du croupier (affichage du résultat)
            pointJoueur = self.game.pointage(self.game.joueur)
            pointCroupier = self.game.pointage(self.game.croupier)

            if self.game.isCroupier == 1:
                # Logique de fin de partie
                if pointCroupier == pointJoueur:
                    null = INPUT_FONT.render("Partie nulle", True, WHITE)
                    self.SCREEN.blit(null, (self.SCREEN_WIDTH // 3, self.SCREEN_HEIGHT // 2))
                    if time - self.game.maintenant >= 10000:
                        self.game.fond += self.game.mise
                        self.game.mise = 0
                        self.miser = 1
                elif pointCroupier > pointJoueur and pointCroupier <= 21:
                    txt = INPUT_FONT.render("Perdu", True, WHITE)
                    self.SCREEN.blit(txt, (self.SCREEN_WIDTH // 3, self.SCREEN_HEIGHT // 2))
                    if time - self.game.maintenant >= 10000:
                        self.game.mise = 0
                        self.miser = 1
                elif pointCroupier > 21:
                    txt = INPUT_FONT.render("Victoire", True, WHITE)
                    self.SCREEN.blit(txt, (self.SCREEN_WIDTH // 3, self.SCREEN_HEIGHT // 2))
                    if time - self.game.maintenant >= 10000:
                        self.game.fond += 2 * self.game.mise
                        self.game.mise = 0
                        self.miser = 1

            # Affichage des cartes du croupier
            for i in range(len(self.game.croupier)):
                if i == 1 and self.game.isCroupier == 0:
                    # Deuxième carte cachée

                    self.SCREEN.blit(pygame.transform.scale(self.game.dos[0], (242//n, 340//n)), (self.SCREEN_WIDTH // 3 + 70, 100))
                else:

                    self.SCREEN.blit(pygame.transform.scale(self.game.croupier[i][2], (242//n, 340//n)), (self.SCREEN_WIDTH // 3 +(i * 70), 100))

            # Affichage des cartes du joueur
            for i in range(0, len(self.game.joueur)):

                self.SCREEN.blit(pygame.transform.scale(self.game.joueur[i][2], (242//n, 340//n)), (self.SCREEN_WIDTH // 3 + (i * 70 ), self.SCREEN_HEIGHT / 1.7))

            # Affichage du paquet de pioche
            for i in range(self.game.nbr_c):
                # Réduire le décalage pour l'effet de pile

                self.SCREEN.blit(pygame.transform.scale(self.game.dos[1], (242//n, 340//n)), (50 + i * 1 , 0))

            # Logique de BUSTED du joueur
            if pointJoueur > 21:
                txt = INPUT_FONT.render("BUSTED", True, WHITE)
                self.SCREEN.blit(txt, (self.SCREEN_WIDTH // 3, self.SCREEN_HEIGHT // 2))
                if time - self.game.maintenant >= 10000:
                    self.game.mise = 0
                    self.miser = 1
            # Logique de BLACKJACK
            if self.isblackjack == 1:
                blackjack_txt = INPUT_FONT.render("BlackJack", True, WHITE)
                self.SCREEN.blit(blackjack_txt, (self.SCREEN_WIDTH // 3, self.SCREEN_HEIGHT // 2))
                if time - self.game.maintenant >= 5000:
                    self.game.fond += int(2.5 * self.game.mise)
                    self.game.mise = 0
                    self.miser = 1
                    self.isblackjack = 0

            # Affichage des boutons si le jeu n'est pas en cours de vérification ou terminé
            if self.game.isCroupier == 0 and pointJoueur <= 21:
                for button in self.buttons_jeu:
                    button.draw(self.SCREEN)

    def jeu(self):
        time = pygame.time.get_ticks()

        # 1. Vérification de l'animation
        if self.animator.is_animating:
            # Si l'animation est en cours, on dessine l'état statique, puis l'animation par-dessus
            self.dessiner_jeu_statique(time)
            self.animator.draw(self.SCREEN)
            # Tente de mettre à jour l'animation. S'il retourne False, c'est qu'elle est terminée.
            if not self.animator.update():
                self.STATE = "Jouer" # Revenir à l'état de jeu normal
            return

        # 2. Logique normale si aucune animation en cours
        self.dessiner_jeu_statique(time)

        # 3. Logique de tirage automatique du croupier après la vérification
        # (seulement si le joueur n'a pas busté et n'a pas BlackJack)
        if self.game.isCroupier == 1 and self.isblackjack == 0 and self.game.pointage(self.game.joueur) <= 21:
            pointCroupier = self.game.pointage(self.game.croupier)
            pointJoueur = self.game.pointage(self.game.joueur)

            # Le croupier tire tant que son score est inférieur au score du joueur ET inférieur à 17
            if pointCroupier < 17 and pointCroupier < pointJoueur:
                # On déclenche une animation de tirage pour le croupier
                self.animate_draw(is_croupier=True)
                return # On arrête pour laisser l'animation se jouer
            elif pointCroupier < 17 and pointCroupier < 21:
                 # Règle typique du blackjack : le croupier doit tirer jusqu'à 17 ou plus
                self.animate_draw(is_croupier=True)
                return

    def animate_draw(self, is_croupier=False):
        # Vérifiez que le paquet a des cartes
        if not self.game.carte:
            print("Plus de cartes dans le paquet!")
            return

        if self.animator.is_animating:
            return

        # 1. Tirer la carte AVANT de commencer l'animation
        card = self.game.partager()
        if card is None: # Vérification supplémentaire
            print("Erreur: carte piochée est None")
            return

        n = 4 # Facteur de taille de carte

        # 2. Ajouter la carte à la main appropriée
        if is_croupier:
            self.game.croupier.append(card)
            face_up = True # Le croupier révèle toujours ses cartes après le tour du joueur
            target_x = self.SCREEN_WIDTH // 3 + ((len(self.game.croupier) - 1) * 70)
            target_y = 100
        else:
            self.game.joueur.append(card)
            face_up = True
            target_x = self.SCREEN_WIDTH // 3 + ((len(self.game.joueur) - 1) * 70)
            target_y = self.SCREEN_HEIGHT / 1.7

        self.game.nbr_c = len(self.game.carte) # Mise à jour du compteur de cartes restantes

        # 3. Démarrer l'animation
        self.animator.start_animation(card, (target_x, target_y), face_up)
        # 4. Passer à l'état de pioche pour bloquer les autres actions
        self.STATE = "Drawing"


class CardAnimator:
    def __init__(self, screen_width, screen_height, start_pos,dos_image):
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
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



if __name__ == "__main__":
    game_princ = GameEngine()
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or game_princ.STATE == "Quitter":
                running = False
                game_princ.game.sauvegarder(game_princ.game.nom, game_princ.game.fond)
                pygame.time.delay(500)
            if game_princ.STATE == "Menu":
                for button in game_princ.buttons_menu:
                    button.handle_event(event)
            # Mise à jour de la gestion des événements pour l'état "Drawing"
            if game_princ.STATE == "Jouer" or game_princ.STATE == "Drawing":
                if game_princ.miser == 1:
                    for button in game_princ.buttons_jeuMise:
                        button.handle_event(event)
                # Ne pas traiter les boutons de jeu si on est en train de miser ou si une animation est en cours
                elif game_princ.isblackjack == 0 and game_princ.game.isCroupier == 0 and game_princ.STATE == "Jouer":
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
        # Mise à jour de la boucle de dessin pour l'état "Drawing"
        elif game_princ.STATE == "Jouer" or game_princ.STATE == "Drawing":
            game_princ.jeu()
        elif game_princ.STATE == "Pause":
            game_princ.pause()

        pygame.display.flip()
        clock.tick(30) # Augmenter la fréquence pour une animation plus fluide (30 à 60 FPS)

pygame.quit()