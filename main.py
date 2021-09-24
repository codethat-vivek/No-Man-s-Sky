import pygame
from pygame import mixer
import random
import math

# Initialising pygame
pygame.init()

# Width and Height of the pygame window
WIDTH = 800
HEIGHT = 600

# # Color
# BACKGROUND_COLOR = (11, 238, 207)

# Creating a Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Background Image(Load)
background = pygame.image.load('background.jpg')
# Background Sound
mixer.music.load('Dangerous1.mp3')
mixer.music.play(-1)

# Adding the Title and Icon to the pygame window
pygame.display.set_caption("No Man's Sky")
icon = pygame.image.load('alien.png')
pygame.display.set_icon(icon)

# bool var
running = True

# Score Creation text on Screen
score_value = 0
font = pygame.font.Font('Albertho.ttf', 40)


# Displays the score
def show_score():
    score = font.render("Score :" + str(score_value), True, (0, 255, 0))
    screen.blit(score, (0, 0))


# Displays the game_over text
over_font = pygame.font.Font('Milletun.otf', 64)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (250, 250))


# Player
# Loads the image(64*64) of the player
playerImg = pygame.image.load('aircraft.png')
playerX = 360
playerY = 500
playerX_Change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_Change = []
enemyY_Change = []
num_of_enemies = 4
for i in range(num_of_enemies):
    enemyImg.append((pygame.image.load('spaceship.png')))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_Change.append(4)
    enemyY_Change.append(25)


# Bullet
# Loads the image(32*32) of the bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 500
bulletX_Change = 0
bulletY_Change = 5
# Bullet has two states:
# Ready state = It is ready to be fire but can not be seen right now
# Fire state = The bullet is fired and is currently moving
bullet_state = "ready"


# function for drawing the player image and setting it's position
def player(x, y):
    screen.blit(playerImg, (x, y))


# function for drawing the enemy image nad setting it's position
def enemy(x, y, idx):
    screen.blit(enemyImg[idx], (x, y))


# function for firing the bullets from the aircraft
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16, y+10))


# Function that detects collision between the bullet and enemy
def detect_collision(ex, ey, bx, by):
    # ex - enemyX, ey - enemyY, bx - bulletX, by - bulletY
    distance = math.sqrt(math.pow(ex - bx, 2) + math.pow(ey - by, 2))
    # 27 came from trial and error
    if distance < 27:
        return True
    return False


# Game Loop
while running:
    # # Fills the screen with the BACKGROUND_COLOR
    # screen.fill(BACKGROUND_COLOR)

    # Background Image
    # Loading of this background, every time the while loop runs
    # slows down the movement speed of the player and the enemy object.
    # Therefore the value of playerX_Change and enemyX_Change has been increased to 5 and 4 respectively.
    screen.blit(background, (0, 0))

    # Event is anything that is happening in the pygame window,
    # For ex- moving our mouse, if we press any key on the keyboard, even exiting the pygame window is an event.
    for event in pygame.event.get():
        # Holds the pygame window until the user closes it
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # check whether keystroke pressed is right or left:
            if event.key == pygame.K_LEFT:
                playerX_Change -= 5
            if event.key == pygame.K_RIGHT:
                playerX_Change += 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    # Get the current x coordinate of the aircraft
                    bulletX = playerX
                    fire_bullet(bulletX, playerY)
        # Key stroke has been released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_Change = 0

    # Checking for boundaries of spaceship(player) so that it doesn't go out of bounds
    playerX += playerX_Change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement oscillates between the pygame window
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 490:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_Change[i]
        if enemyX[i] <= 0:
            enemyX_Change[i] = 4
            enemyY[i] += enemyY_Change[i]
        elif enemyX[i] >= 736:
            enemyX_Change[i] = -4
            enemyY[i] += enemyY_Change[i]

        # Collision
        collision = detect_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        # If collision happens
        if collision:
            # explosion_sound = mixer.Sound('Explosion.wav')
            # explosion_sound.play()
            bulletY = 500
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    # This if-loop ensures the firing of multiple bullets from the aircraft
    if bulletY <= 0:
        bulletY = 500
        bullet_state = "ready"
    # Infinite loop where the bullet's y-coordinate decreases which shows the movement of bullet
    if bullet_state == "fire":
        bullet_sound = mixer.Sound('Gunshot.wav')
        bullet_sound.play()
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_Change

    player(playerX, playerY)
    show_score()
    # Updates the display i.e the pygame window, IT'S A NECESSITY
    pygame.display.update()
