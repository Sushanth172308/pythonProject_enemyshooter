import pygame
import random
import math

# intializing pygame
pygame.init()

# creating  a window for pumpkinshooter

screen = pygame.display.set_mode((800, 600))

# Adding Titles and icons
title = 'Pumpkin Shooter'
icon = pygame.image.load('data/icon.png')
pygame.display.set_caption(title)
pygame.display.set_icon(icon)

# Adding background image
bg = pygame.image.load('data/background.jpg')
pygame.mixer.music.load('data/bmusic.wav')
pygame.mixer.music.play(-1)

bullet_sound = pygame.mixer.Sound('data/laser.wav')
explosion_sound = pygame.mixer.Sound('data/explo.wav.')

# Player
player_img = pygame.image.load('data/player.png')
# playerX = 400-32
playerX = 368
# playerY = 600-64-20
playerY = 516
playerX_change = 0

# multiple Enemies
num_of_enemies = 6
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load('data/enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(20, 120))
    enemyX_change.append(0.6)
    enemyY_change.append(40)

'''
# creating Enemy
enemy_img = pygame.image.load('data/enemy.png')
#enemyX = 736   #800-64
enemyX = random.randint(0, 736)
enemyY = random.randint(20, 120)
enemyX_change = 0.5
enemyY_change = 40
'''
# bullet

bullet_img = pygame.image.load('data/bullet.png')
bulletX = 0
bulletY = 516
bulletY_change = -1.0
bullet_state = 'ready'

score = 0

score_font = pygame.font.Font('data/Aldrich-Regular.ttf', 32)
scoreX = 10
scoreY = 10

game_over_font = pygame.font.Font('data/Aldrich-Regular.ttf', 64)
game_overX = 200
game_overY = 200

restart_font = pygame.font.Font('data/Aldrich-Regular.ttf', 40)
restartX = 100
restartY = 300

game_status = 'running'


def show_restart(x, y):
    restart_img = restart_font.render('To restart the Game press R ', True, (0, 255, 0))
    screen.blit(restart_img, (x, y))


def show_game_over(x, y):
    global game_status
    game_over_img = game_over_font.render('GAME OVER ', True, (255, 255, 255))
    screen.blit(game_over_img, (x, y))
    pygame.mixer.music.stop()
    game_status = 'end'


def show_score(x, y):
    score_img = score_font.render('Score: ' + str(score), True, (255, 255, 255))
    screen.blit(score_img, (x, y))


# using distnce between two coordinates(Enemy & bullet)
def isCollistion(x1, y1, x2, y2):
    distance = math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))
    if distance < 25:
        return True
    else:
        return False


def bullet(x, y):
    # screen.blit(bullet_img, (x, y))
    screen.blit(bullet_img, (x + 10, y + 10))


# creating  a function for screen.blit to reuse
def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


# creating  a function for screen.blit to reuse
def player(x, y, ):
    screen.blit(player_img, (x, y))


game_on = True
while game_on:
    # Background RGB
    screen.fill((71, 63, 82))
    screen.blit(bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_on = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                print('LEFT Arrow is pressed')
                playerX_change = -0.7
            if event.key == pygame.K_RIGHT:
                print('RIGHT Arrow is pressed')
                playerX_change = 0.7

            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_state = 'fire'
                    bulletX = playerX
                    bullet(bulletX, bulletY)
                    bullet_sound.play()
                # Restarting the GAME
            if event.key == pygame.K_r:
                if game_status == 'end':
                    game_status = 'running'
                    score = 0
                    playerX = 368
                    pygame.mixer.music.play(-1)

                    for i in range(num_of_enemies):
                        enemyX[i] = random.randint(0, 736)
                        enemyY[i] = random.randint(20, 120)

                    # print('Game Restarted')
            #   bullet(playerX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Bullet Movements
    if bullet_state == 'fire':
        if bulletY < 10:
            bulletY = 516
            bullet_state = 'ready'
        bulletY += bulletY_change
        bullet(bulletX, bulletY)
    # bullet(playerX, bulletY)

    # Enemy movements
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 466:
            show_game_over(game_overX, game_overY)
            show_restart(restartX, restartY)
            for j in range(num_of_enemies):
                enemyY[j] = 1200
        # ****
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX[i] = 0
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:  # 800-64  width of back ground - width of player
            enemyX[i] = 736
            enemyX_change[i] = -0.8
            enemyY[i] += enemyY_change[i]

        enemy(enemyX[i], enemyY[i], i)

        # Collusion:
        collision = isCollistion(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 516
            bullet_state = 'ready'
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(20, 120)
            score += 1
            explosion_sound.play()
            # print(score)

    show_score(scoreX, scoreY)

    #    screen.blit(player_img, (playerX, playerY))
    # player movements
    playerX += playerX_change
    #  creating boundary of left and right
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:  # 800-64  width of back ground - width of player
        playerX = 736

    player(playerX, playerY)

    pygame.display.update()
