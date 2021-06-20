import pygame
import math
import random
import movies_list

pygame.init()

# setup display
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman - Movie Version")

# load images
images = []
for i in range(7):
    image = pygame.image.load("images/Stage" + str(i+1) + ".png")
    images.append(image)

# button variables
RADIUS = 20
GAP = 15
letters = []
start_X = round((WIDTH - (RADIUS * 2 + GAP) * 12 - 2 * RADIUS) / 2)
start_Y = 450
A = 65
for i in range(26):
    x = start_X + RADIUS + ((RADIUS * 2 + GAP) * (i % 13))
    y = start_Y + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

# fonts
LETTER_FONT = pygame.font.SysFont("comicsansms", 25)
WORD_FONT = pygame.font.SysFont("consolas", 25)
RESULT_FONT = pygame.font.SysFont("Cambria", 40)
TITLE_FONT = pygame.font.SysFont("Cambria", 60)

# game variables
hangman_status = 0
word = random.choice(movies_list.movies).upper()
characters = "".join(set(word))
no_of_characters = len(characters)
guessed = []
for letter in characters:
    asc = ord(letter)
    if not (asc >= 65 and asc <= 90):
        guessed.append(letter)

# colors
BG_COLOR = (237, 237, 237)
WORD_COLOR = (218, 0, 55)
LETTER_COLOR = (68, 68, 68)

# setup game loop
FPS = 60
clock = pygame.time.Clock()
run = True


def draw():
    win.fill(BG_COLOR)

    # draw title
    text = TITLE_FONT.render("HANGMAN", 1, WORD_COLOR)
    win.blit(text, ((WIDTH - text.get_width()) / 2, 20))
    # draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, WORD_COLOR)
    win.blit(text, (400, 200))

    # draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, LETTER_COLOR, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, LETTER_COLOR)
            win.blit(text, (x - text.get_width() /
                     2, y - text.get_height() / 2))

    # draw images
    win.blit(images[hangman_status], (50, 100))
    pygame.display.update()


def resultMsg(message):
    win.fill(BG_COLOR)
    text = RESULT_FONT.render(message, 1, WORD_COLOR)
    win.blit(text, ((WIDTH - text.get_width()) /
             2, (HEIGHT - text.get_height()) / 2))
    text = WORD_FONT.render(word, 1, WORD_COLOR)
    win.blit(text, ((WIDTH - text.get_width()) /
             2, (HEIGHT - text.get_height()) / 2 + 50))
    win.blit(images[hangman_status], (50, 100))
    pygame.display.update()
    pygame.time.delay(5000)


while run:
    clock.tick(FPS)
    draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            m_X, m_Y = pygame.mouse.get_pos()
            for letter in letters:
                x, y, ltr, visible = letter
                if visible:
                    dis = math.sqrt((x - m_X) ** 2 + (y - m_Y) ** 2)
                    if dis < RADIUS:
                        if ltr in word:
                            guessed.append(ltr)
                        else:
                            hangman_status += 1
                        letter[3] = False

    if len(guessed) == no_of_characters:
        resultMsg("You WON!")
        break
    elif hangman_status >= 6:
        resultMsg("You LOSE!")
        break

pygame.quit()
