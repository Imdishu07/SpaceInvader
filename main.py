import math
import random

import pygame
from pygame import mixer

pygame.init()                                             # Initialize the pygame here

screen = pygame.display.set_mode((800, 600))              # create the screen

background = pygame.image.load('background.jpg')          # Background

mixer.music.load("background.wav")                        # Sound
mixer.music.play(-1)

pygame.display.set_caption("Space Invader")               # Caption and Icon
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

playerImg = pygame.image.load('player.png')                # Player
playerX = 370
playerY = 480
playerX_change = 0

enemyImg = []                                              # Enemy
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 10

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.4)
    enemyY_change.append(20)

bulletImg = pygame.image.load('bullet.png')                  # Bullet
                                                             # Ready - You can't see the bullet on the screen
                                                             # Fire - The bullet is currently moving
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.4
bullet_state = "ready"

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):                                                                  # score
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():                                                                  # game over
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16, y+10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


running = True                                            # game loop
while running:

    screen.fill((0, 0, 0))                                # Red, Green and Blue = RGB

    screen.blit(background, (0, 0))                       # background image
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:                   # if keystroke is pressed check whether its right or left
            if event.key == pygame.K_LEFT:
                playerX_change = -0.4
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.4
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()

                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_of_enemies):                     # Enemy Movement

        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)          # collision
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0:                                                               # Bullet Movement
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()

