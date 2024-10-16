import pygame
from pygame import *
import random
import time

# Initialize pygame and mixer
pygame.init()
mixer.init()

# Dynamic screen resolution with 16:9 aspect ratio
screen_width = pygame.display.Info().current_w
screen_height = int(screen_width * 9 / 16)  # Maintain 16:9 aspect ratio
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Blackjack")

# Sounds and Music
drawS = mixer.Sound("sound/draw.mp3")
mixer.music.load("sound/background_music.mp3")
mixer.music.play(-1)

# Game state variables
can_draw = True
startMenu = True
gameon = False
button_hide = False

player_deck = []
casino_deck = []
player_score = 0
casino_score = 0

# Dynamic scaling factor for images and fonts
scale_x = screen_width / 1280/2
scale_y = screen_height / 720/2

# Font for the game (scaled)
font = pygame.font.SysFont(None, int(40 * scale_x))  # Adjusted font size

# Preload images with scaling
def load_image(path, scale_x, scale_y):
    img = pygame.image.load(path)
    img = pygame.transform.scale(img, (int(img.get_width() * scale_x), int(img.get_height() * scale_y)))
    return img

# Load UI images
quitB = load_image("Art/Ui/quitB.jpg", scale_x, scale_y)
startB = load_image("Art/Ui/startB.jpg", scale_x, scale_y)
backB = load_image("Art/Ui/backB.jpg", scale_x, scale_y)
hitB = load_image("Art/Ui/hit.jpg", scale_x, scale_y)
stayB = load_image("Art/Ui/stay.jpg", scale_x, scale_y)
MenuBackground = load_image("Art/Ui/background.jpg", scale_x, scale_y)
GameonBackground = load_image("Art/Ui/gameon.jpg", scale_x, scale_y)
victory = load_image("Art/victory.jpg", scale_x, scale_y)
defeat = load_image("Art/defeat.jpg", scale_x, scale_y)
draw = load_image("Art/draw.jpg", scale_x, scale_y)

# Card images cache (preloading card images)
def load_card_images():
    suits = ["pique", "trefle", "diamond", "coeur"]
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "j", "q", "k", "as"]
    card_images = {}
    for suit in suits:
        for value in values:
            card_name = f"{value} de {suit}"
            card_images[card_name] = load_image(f"Art/cards/{card_name}.png", scale_x, scale_y)
    return card_images

card_images = load_card_images()

# Text class for displaying text
class Text:
    def __init__(self, context, color):
        self.context = font.render(context, True, color)

    def draw(self, x, y):
        screen.blit(self.context, (x * scale_x, y * scale_y))

# Button class for interactive UI elements
class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * scale_x, y * scale_y)

    def draw(self):
        screen.blit(self.image, self.rect.topleft)

# Create buttons
quitButton = Button(720 // 2 - 130, int(1000 * scale_y), quitB)
startButton = Button(720 // 2 - 130, int(500 * scale_y), startB)
backButton = Button(int(610 * scale_x), int(1000 * scale_y), backB)
hitButton = Button(int(50 * scale_x), int(1000 * scale_y), hitB)
stayButton = Button(int(350 * scale_x), int(1000 * scale_y), stayB)

# Card deck functions
def card_deck52():
    colors = ["pique", "trefle", "diamond", "coeur"]
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "j", "q", "k", "as"]
    deck = [f"{value} de {color}" for color in colors for value in values]
    return deck

def reset_game():
    global player_deck, casino_deck, player_score, casino_score, cards52
    player_deck = []
    casino_deck = []
    player_score = 0
    casino_score = 0
    cards52 = card_deck52()

# Calculate the score of a deck
def score(deck):
    score = 0
    for card in deck:
        value = card.split(" ")[0]
        if value in ["k", "q", "j"]:
            score += 10
        elif value == "as":
            score += 11
        else:
            score += int(value)
    return score

# Pick a random card from the deck
def pioche(cards, play_sound=False):
    card = random.choice(cards)
    cards.remove(card)
    if play_sound:
        try:
            drawS.play()
        except Exception as e:
            print("Sound error:", e)
    return card

# Player and casino actions
def first_draw():
    global player_score
    player_deck.append(pioche(cards52))
    player_deck.append(pioche(cards52))
    player_score = score(player_deck)

def first_draw_casino():
    global casino_score
    casino_deck.append(pioche(cards52))
    casino_score = score(casino_deck)

def player_draw():
    global player_score
    player_deck.append(pioche(cards52, play_sound=True))
    player_score = score(player_deck)

def casino_draw():
    global casino_score
    casino_deck.append(pioche(cards52, play_sound=True))
    casino_score = score(casino_deck)

# Display game result
def display_result(result_image):
    screen.blit(result_image, (int(218 * scale_x), int(576 * scale_y)))

# Game loop
running = True
reset_game()

while running:
    screen.fill((0, 0, 0))  # Clear the screen
    mouse_pos = pygame.mouse.get_pos()

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if quitButton.rect.collidepoint(mouse_pos):
                running = False
            if startButton.rect.collidepoint(mouse_pos) and startMenu:
                startMenu = False
                gameon = True
                reset_game()
                first_draw()
                first_draw_casino()
            if hitButton.rect.collidepoint(mouse_pos) and can_draw:
                player_draw()
            if stayButton.rect.collidepoint(mouse_pos):
                can_draw = False

    # Start menu
    if startMenu:
        screen.blit(MenuBackground, (0, 0))
        quitButton.draw()
        startButton.draw()
        stollymine = Text("Made by stollymine", "black")
        stollymine.draw(180, int(1140 * scale_y))

    # Game screen
    if gameon:
        screen.blit(GameonBackground, (0, 0))
        backButton.draw()
        if can_draw and not button_hide:
            hitButton.draw()
            stayButton.draw()

        # Player and casino card displays
        for i, card in enumerate(player_deck):
            screen.blit(card_images[card], (300 + i * 100 * scale_x - 35 * len(player_deck) * scale_x, int(900 * scale_y)))

        for i, card in enumerate(casino_deck):
            screen.blit(card_images[card], (300 + i * 100 * scale_x - 20 * len(casino_deck) * scale_x, int(200 * scale_y)))

        # Scores
        player_score_text = Text(f"Your Score: {player_score}", "black")
        player_score_text.draw(100, int(833 * scale_y))
        casino_score_text = Text(f"Casino Score: {casino_score}", "black")
        casino_score_text.draw(100, int(533 * scale_y))

        # Game result checks
        if player_score == 21:
            display_result(victory)
            button_hide = True
        elif player_score > 21:
            display_result(defeat)
            button_hide = True
        elif can_draw == False and casino_score >= 16:
            if player_score > casino_score or casino_score > 21:
                display_result(victory)
            elif player_score < casino_score:
                display_result(defeat)
            else:
                display_result(draw)
            button_hide = True

    pygame.display.update()

pygame.quit()
