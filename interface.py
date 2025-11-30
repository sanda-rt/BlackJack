import pygame
import sys

# --- Configuration de base ---
pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blackjack Classique")
icon = pygame.image.load("Image/icone.png")
pygame.display.set_icon(icon)

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (50, 50, 50)
LIGHT_BEIGE = (210, 180, 140)
DARK_BEIGE = (180, 150, 110)
GREEN_TABLE = (0, 128, 0)

# Polices
TITLE_FONT = pygame.font.Font(None, 100)
BUTTON_FONT = pygame.font.Font(None, 40)
INPUT_FONT = pygame.font.Font(None, 35)

# --- Classes d'éléments d'interface ---
class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.color_normal = DARK_GRAY
        self.color_hover = DARK_BEIGE
        self.current_color = self.color_normal

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        self.current_color = self.color_hover if self.rect.collidepoint(mouse_pos) else self.color_normal
        pygame.draw.rect(surface, self.current_color, self.rect, border_radius=5)
        text_surf = BUTTON_FONT.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()
                return True
        return False

class TextBox:
    def __init__(self, x, y, width, height, placeholder=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_active = LIGHT_BEIGE
        self.color_passive = DARK_GRAY
        self.color = self.color_passive
        self.text = ''
        self.placeholder = placeholder
        self.active = False
        self.text_color = BLACK

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.color = self.color_active
            else:
                self.active = False
                self.color = self.color_passive

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                print(f"Pseudo entré: {self.text}")
                self.active = False
                self.color = self.color_passive
            else:
                self.text += event.unicode

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=5)
        display_text = self.text if self.text or self.active else self.placeholder
        text_color = self.text_color if self.text else WHITE
        text_surf = INPUT_FONT.render(display_text, True, text_color)
        surface.blit(text_surf, (self.rect.x + 10, self.rect.y + 10))
        if self.active:
            pygame.draw.rect(surface, LIGHT_BEIGE, self.rect, 3, border_radius=5)

# --- Fonctions d'action ---
if __name__ == "__main__":
    def play_game():
        print("Action: JOUER")

    def open_settings():
        print("Action: PARAMÈTRES")
    def show_rules():
        print("Action: RÈGLES du Blackjack affichées ici")

    # --- Éléments du menu principal ---
    PADDING = 20
    BUTTON_WIDTH = 250
    BUTTON_HEIGHT = 60
    BUTTON_START_Y = 250
    BUTTON_SPACING = BUTTON_HEIGHT + PADDING

    pseudo_box = TextBox(
        SCREEN_WIDTH - BUTTON_WIDTH - 50,
        BUTTON_START_Y - 70,
        BUTTON_WIDTH,
        BUTTON_HEIGHT - 10,
        placeholder="Ton pseudo..."
    )

    buttons = [
        Button(pseudo_box.rect.x, BUTTON_START_Y, BUTTON_WIDTH, BUTTON_HEIGHT, "JOUER", play_game),
        Button(pseudo_box.rect.x, BUTTON_START_Y + BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT, "PARAMÈTRES", open_settings),
        Button(pseudo_box.rect.x, BUTTON_START_Y + 2 * BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT, "RÈGLES", show_rules)
    ]


    # --- Chargement background ---
    try:
        BACKGROUND_IMAGE = pygame.image.load('BG_joker.png').convert()
        BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except pygame.error:
        print("Attention: image introuvable, fond noir utilisé")
        BACKGROUND_IMAGE = None

    # --- Chargement musique de fond ---
    try:
        pygame.mixer.music.load("KOOL CATS by Kevin MacLeod.mp3")  # Remplace par ton fichier
        pygame.mixer.music.set_volume(0.2)           # Volume 50%
        pygame.mixer.music.play(-1)                  # Boucle infinie
    except pygame.error:
        print("Attention: musique introuvable ou format non supporté")

    # --- Boucle principale ---
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            pseudo_box.handle_event(event)

            for button in buttons:
                button.handle_event(event)

        # Dessin du menu
        if BACKGROUND_IMAGE:
            SCREEN.blit(BACKGROUND_IMAGE, (0, 0))
        else:
            SCREEN.fill(BLACK)

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        SCREEN.blit(overlay, (0, 0))

        title_surf_1 = TITLE_FONT.render("BLACKJACK", True, LIGHT_BEIGE)
        title_surf_2 = TITLE_FONT.render("21", True, WHITE)
        SCREEN.blit(title_surf_1, (50, 150))
        SCREEN.blit(title_surf_2, (50, 250))

        pseudo_box.draw(SCREEN)

        for button in buttons:
            button.draw(SCREEN)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()
