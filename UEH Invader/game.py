import math
import random

import pygame
from pygame import mixer

game_over = False

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('Terrain/background.png')

# Sound
mixer.music.load("Sounds/background.mp3")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("UEH Invaders")
icon = pygame.image.load('Assets/logo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('Assets/player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemy_types = [pygame.image.load('Assets/enemy1.png'),
               pygame.image.load('Assets/enemy2.png'),
               pygame.image.load('Assets/enemy3.png')]

num_of_enemies = 8
enemy_list = []

for i in range(num_of_enemies):
    enemy_list.append([random.randint(0, 736), random.randint(50, 150), 0.6, 40, random.choice(enemy_types)])

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('Assets/laser.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, enemy_type):
    screen.blit(enemy_type, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
music_playing = True

while running:

    if game_over:
        screen.fill((0, 0, 0))
        game_over_text()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
            
                    # Reset the game
                    playerX = 370
                    playerY = 480
                    score_value = 0
                    bulletY = 480
                    bullet_state = "ready"
                    for i in range(num_of_enemies):
                        enemy_list[i][0] = random.randint(0, 736)
                        enemy_list[i][1] = random.randint(50, 150)
                    game_over = False

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    laser_sound = mixer.Sound("Sounds/laser.wav")
                    laser_sound.play()
                    # Get the current x cordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
            if event.key == pygame.K_m:
                if music_playing:
                    mixer.music.pause()
                else:
                    mixer.music.unpause()
                music_playing = not music_playing

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

        # Check if music should be toggled on or off
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if x >= 10 and x <= 50 and y >= 30 and y <= 90:
                if music_playing:
                    mixer.music.pause()
                else:
                    mixer.music.unpause()
                music_playing = not music_playing

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemy_list[i][1] >350:
            for j in range(num_of_enemies):
                enemy_list[j][1] = 2000
            game_over_text()
            break

        enemy_list[i][0] += enemy_list[i][2]
        if enemy_list[i][0] <= 0:
            enemy_list[i][2] = 0.3
            enemy_list[i][1] += enemy_list[i][3]
        elif enemy_list[i][0] >= 736:
            enemy_list[i][2] = -0.3
            enemy_list[i][1] += enemy_list[i][3]

        # Collision
        collision = isCollision(enemy_list[i][0], enemy_list[i][1], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("Sounds/explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemy_list[i][0] = random.randint(0, 736)
            enemy_list[i][1] = random.randint(50, 150)

        enemy(enemy_list[i][0], enemy_list[i][1], enemy_list[i][4])

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, testY)

    # Draw a button to toggle the background music
    music_icon = pygame.image.load('Assets/mutemusic.png').convert_alpha()
    music_icon_rect = music_icon.get_rect(topleft = (10,50))
    screen.blit(music_icon, music_icon_rect)
    laser_icon = pygame.image.load('Assets/mutelaser.png').convert_alpha()
    laser_icon_rect = laser_icon.get_rect(topleft = (10,100))
    screen.blit(laser_icon, laser_icon_rect)
    pygame.display.update()
    