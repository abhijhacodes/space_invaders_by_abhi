import pygame
import random
import math
from pygame import mixer

# initialize pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((800, 600))

# title and icon
pygame.display.set_caption('Space Invaders by Abhi')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# background image
background = pygame.image.load('background.png')

# background sound
mixer.music.load('bg.mp3')
mixer.music.play(-1)
# due to -1 in parameter, music plays in loop

# creating player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 36)
textX = 10
textY = 10


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (0, 255, 100))
    screen.blit(score, (x, y))


# game over
over_font = pygame.font.Font('freesansbold.ttf', 70)


def game_over(fin_score):
    over = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over, (170, 220))
    final_score = font.render("Your final score: " + str(fin_score), True, (0, 255, 100))
    screen.blit(final_score, (210, 290))
    play_again = font.render("Thank you for playing", True, (0, 255, 100))
    screen.blit(play_again, (190, 330))
    pygame.display.update()
    mixer.music.stop()


# creating enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 10

for i in range(no_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(10, 50))
    enemyX_change.append(6)
    enemyY_change.append(40)


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# creating bullet to shoot
# state - ready(can't see bullet on screen)
# fire(bullet is currently moving on screen)
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 18
bullet_state = 'ready'


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    # when bullet is in fire state, blitting the bullet in motion
    screen.blit(bulletImg, (x + 16, y + 10))
    # changing value of a and y so that it shoots from center of player


# detecting collision, when distnce between bullet and enemy is
# relatively low it will return true
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# pause function
paused = False


# to pause the screen while playing and display various navigation options,
# i.e. continue and quit
def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False

                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        # displaying various options on paused screen
        screen.fill((255, 255, 255))
        pause_font = pygame.font.Font('freesansbold.ttf', 70)
        pFont = pause_font.render("GAME PAUSED", True, (0, 0, 0))
        screen.blit(pFont, (150, 220))
        ins_font = pygame.font.Font('freesansbold.ttf', 30)
        iFont = ins_font.render("Press C to continue or Q to quit.", True, (0, 0, 0))
        screen.blit(iFont, (170, 320))
        pygame.display.update()


# game loop that runs until we close game window
if __name__ == '__main__':
    running = False  # game variable to define state of the game

    # to display message until we press any key and then start the game
    while not running:
        welcome = pygame.image.load('welcome.png')
        screen.blit(welcome, (0, 0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                running = True

    # main game loop
    while running:
        screen.fill((0, 0, 0))  # r-g-b value of colour
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # to close
                running = False

            if event.type == pygame.KEYDOWN:
                # player movement
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    playerX_change = -10
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    playerX_change = 10

                # firing bullet
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    bullet_sound = mixer.Sound('gunfire.mp3')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

                # to pause while playing
                if event.key == pygame.K_p:
                    pause()

            # to stop player movement
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                    playerX_change = 0

        # checking boundaries of spaceship player
        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 700:
            playerX = 700

        # handling enemies
        for i in range(no_of_enemies):

            # Game over when any enemy goes beyond the limit on Y axis
            if enemyY[i] > 440:
                for j in range(no_of_enemies):
                    enemyY[j] = 2000  # to make it disappear
                screen.fill((255, 0, 0))
                playerX = 2000
                textX = 2000
                over_music = mixer.Sound('gameover.wav')
                over_music.play()
                game_over(score_value)
                break

            # enemy movement
            """when enemy touches any side boundary i.e. <0 or >700, then we need
            to reverse it's direction, i.e. adding change -ve or +ve accordingly
            and every time on touching boundary, it will down by specific amount
            i.e. increasing Y value"""

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 6
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 700:
                enemyX_change[i] = -6
                enemyY[i] += enemyY_change[i]

            # collision
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                collision_sound = mixer.Sound('explosion.wav')
                collision_sound.play()
                bulletY = 480
                # bulletY = 480 will restore the bullet position to top of spaceship player
                # making the bullet ready to fire again
                bullet_state = "ready"
                score_value += 1  # increasing score everytime on collision
                enemyX[i] = random.randint(0, 700)
                enemyY[i] = random.randint(50, 150)
                # after collision bliting the enemy on random position again

            enemy(enemyX[i], enemyY[i], i)

        # bullet movement
        if bulletY <= 0:
            bulletY = 480  # making ready after fire
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        # blitting player, score on specified position on every iteration of game loop
        player(playerX, playerY)
        show_score(textX, textY)
        pygame.display.update()  # updating screen whenever there is change on it
