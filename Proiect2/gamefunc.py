import button as button
import time
import pygame
import math
import random
import requests
from bs4 import BeautifulSoup

# Crearea displayului
pygame.init()
LATIME, INALTIME = 1000, 800
win = pygame.display.set_mode((LATIME, INALTIME))
pygame.display.set_caption("Spanzuratoarea!")

# Crearea butoanelor
RADIUS = 20
DECALAJ = 15
litere = []
startx = round((LATIME - (RADIUS * 2 + DECALAJ) * 13) / 2)
starty = 400
A = 65
for i in range(26):
    x = startx + DECALAJ * 2 + ((RADIUS * 2 + DECALAJ) * (i % 13))
    y = starty + ((i // 13) * (DECALAJ + RADIUS * 2))
    litere.append([x, y, chr(A + i), True])

# Fonturile folosite
FONT_LITERE = pygame.font.SysFont('comicsans', 40)
FONT_CUVANT = pygame.font.SysFont('comicsans', 60)
FONT_TITLU = pygame.font.SysFont('comicsans', 70)

# incarcam imaginile
images = []
for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)

# Variabilele Jocului
hangman_status = 0
ghicit = []

# Culori
ALB = (255, 255, 255)
NEGRU = (0, 0, 0)

#functia prin care se deseneaza jocul
def draw():
    win.fill(ALB)

    # Titlu
    text = FONT_TITLU.render("SPANZURATOAREA", 1, NEGRU)
    win.blit(text, (LATIME / 2 - text.get_width() / 2, 20))

    # Cuvant
    display_word = ""
    for letter in cuvant:
        if letter in ghicit:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = FONT_CUVANT.render(display_word, 1, NEGRU)
    win.blit(text, (400, 200))

    # Butoane
    for letter in litere:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, NEGRU, (x, y), RADIUS, 3)
            text = FONT_LITERE.render(ltr, 1, NEGRU)
            win.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

    win.blit(images[hangman_status], (150, 100))
    pygame.display.update()

#functia care genereaza mesajele/cuvintele
def display_message(message):
    pygame.time.delay(1000)
    win.fill(ALB)
    text = FONT_CUVANT.render(message, 1, NEGRU)
    win.blit(text, (LATIME / 2 - text.get_width() / 2, INALTIME / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(300)

#resetam toate valorile variabilelor
def clear():
    #de la url ul specificat se acceseaza dictionarul online, de la o comanda de tip request
    url = 'https://randomword.com/'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    global cuvant
    cuvant = soup.find(id='random_word').text.upper()
    #afisam in consola cuvantul generat
    print(cuvant)

    #resetam vectorul care salveaza literele ghicite din cuvant
    global ghicit
    ghicit.clear()

    #resetam spanzuratul
    global hangman_status
    hangman_status = 0

    #resetam ca toate literele sa fie afisate
    for letter in litere:
        letter[3] = True

#functia care ruleaza jocul
def play():
    global hangman_status

    FPS = 60
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in litere:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
                        if dis < RADIUS:
                            letter[3] = False
                            ghicit.append(ltr)
                            if ltr not in cuvant:
                                hangman_status += 1

        draw()

        won = True
        for letter in cuvant:
            if letter not in ghicit:
                won = False
                break

        if won:

            time.sleep(5)
            return



        if hangman_status == 6:
            display_message("Ai pierdut!")
            time.sleep(5)
            return