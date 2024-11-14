# Example file showing a circle moving on screen
import pygame
import random
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
ball_dir = pygame.Vector2(300, 300)
player_pos = pygame.Vector2(30, 30)
globScore = 0

def drawObjects():
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    pygame.draw.rect(screen, "white", pygame.Rect(screen.get_width() - 30, 0, 60, screen.get_height()))
    pygame.draw.rect(screen, "white", pygame.Rect(0, 0, screen.get_width() - 30, 30))
    pygame.draw.rect(screen, "white", pygame.Rect(0, screen.get_height() - 30, screen.get_width(), 30))

    pygame.draw.circle(screen, "white", ball_pos, 20)

    #Player
    pygame.draw.rect(screen, "red", pygame.Rect(player_pos.x - 30, player_pos.y, 30, screen.get_height() / 6))

    #Print score
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render("Score " + str(globScore), True, "white", "black")
    textRect = text.get_rect()
    textRect.center = (screen.get_width() // 2, screen.get_height() // 8)
    screen.blit(text, textRect)

def ballMovement(dt):
    #Ball Collision

    global globScore
    global running
    temp_pos = pygame.Vector2(ball_pos.x + ball_dir.x * dt, ball_pos.y + ball_dir.y * dt)

    if (temp_pos.x <= 50):
        if (temp_pos.y >= player_pos.y - 5):
            if (temp_pos.y <= player_pos.y + screen.get_height() / 6 + 5):
                globScore += 1
                temp_pos.x = 50
                ball_dir.x = -1 * ball_dir.x + random.randint(-5,5)
                ball_dir.y = 1 * ball_dir.y + random.randint(-5,5)
                
    if (temp_pos.x <= 0):
        running = False

    if (temp_pos.x >= screen.get_width() - 50):
        temp_pos.x = screen.get_width() - 50
        ball_dir.x = -1 * ball_dir.x

    if (temp_pos.y >= screen.get_height() - 50):
        temp_pos.y = screen.get_height() - 50
        ball_dir.y = -1 * ball_dir.y
    
    if (temp_pos.y <= 50):
        temp_pos.y = 50
        ball_dir.y = -1 * ball_dir.y


    return(temp_pos)

def gameMovement(direction, dt):
    #direction = 0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        direction = 1
    if keys[pygame.K_s]:
        direction = -1

    if (direction == 1):
        if (player_pos.y - 300 * dt >= 30):
            player_pos.y -= 300 * dt
        else:
            player_pos.y = 30
    if (direction == -1):
        if (player_pos.y + 300 * dt + (screen.get_height() / 6) <= screen.get_height() - 30):
            player_pos.y += 300 * dt
        else:
            player_pos.y = screen.get_height() - 30 - (screen.get_height() / 6)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    drawObjects()
    ball_pos = ballMovement(dt)
    gameMovement(0, dt)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 1200
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(1200) / 1000



print(globScore)
pygame.quit()
