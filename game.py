# Example file showing a circle moving on screen
import pygame
import random
from classes import *

def drawObjects(screen, player_pos, ball_pos, globScore, trainieNum = -1, genNum = -1):
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    #Drawing the shapes to the screen
    pygame.draw.rect(screen, "white", pygame.Rect(screen.get_width() - 30, 0, 60, screen.get_height()))
    pygame.draw.rect(screen, "white", pygame.Rect(0, 0, screen.get_width() - 30, 30))
    pygame.draw.rect(screen, "white", pygame.Rect(0, screen.get_height() - 30, screen.get_width(), 30))
    pygame.draw.circle(screen, "white", (ball_pos.x, ball_pos.y), 20)
    #Player
    pygame.draw.rect(screen, "red", pygame.Rect(player_pos.x - 30, player_pos.y, 30, screen.get_height() / 6))

    #Print score
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render("Score " + str(globScore), True, "white", "black")
    textRect = text.get_rect()
    textRect.center = (screen.get_width() // 2, screen.get_height() // 8)
    screen.blit(text, textRect)

    #If in training mode
    if genNum != -1:
        #Generation Number
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render("Generation " + str(genNum), True, "white", "black")
        textRect = text.get_rect()
        textRect.center = (screen.get_width() // 4, screen.get_height() // 8)
        screen.blit(text, textRect)

        #Internal Number
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render("Trainie # " + str(trainieNum), True, "white", "black")
        textRect = text.get_rect()
        textRect.center = (3 * (screen.get_width() // 4), screen.get_height() // 8)
        screen.blit(text, textRect)

    pygame.display.flip()

def ballMovement(screenW, screenH, dt, ball_dir, ball_pos, player_pos, running, globScore):
    #Find the next position
    temp_pos = Vec2(ball_pos.x + ball_dir.x * dt, ball_pos.y + ball_dir.y * dt)
    #Check if next position intersects and apply relevent changes to the direction and temp pos
    if (temp_pos.x <= 50):
        if (temp_pos.y >= player_pos.y - 5):
            if (temp_pos.y <= player_pos.y + screenH / 6 + 5):
                globScore += 1
                temp_pos.x = 50
                ball_dir.x = -1 * ball_dir.x + random.randint(-5,5)
                ball_dir.y = 1 * ball_dir.y + random.randint(-5,5)
                
    if (temp_pos.x <= 0):
        running = False

    if (temp_pos.x >= screenW - 50):
        temp_pos.x = screenW - 50
        ball_dir.x = -1 * ball_dir.x

    if (temp_pos.y >= screenH - 50):
        temp_pos.y = screenH - 50
        ball_dir.y = -1 * ball_dir.y
    
    if (temp_pos.y <= 50):
        temp_pos.y = 50
        ball_dir.y = -1 * ball_dir.y

    #I am actually not sure why this is working, I forgot to return the new balls direction
    #I miss C, it yells at me like a proper language when I mess up
    return(temp_pos, running, globScore)

def gameMovement(screenW, screenH, direction, player_pos, dt):
    #Ensures that the player doesnt leave the screen
    if (direction == 1):
        if (player_pos.y - 300 * dt >= 30):
            player_pos.y -= 300 * dt
        else:
            player_pos.y = 30
    if (direction == -1):
        if (player_pos.y + 300 * dt + (screenH / 6) <= screenH - 30):
            player_pos.y += 300 * dt
        else:
            player_pos.y = screenH - 30 - (screenH / 6)

    return(player_pos)

def displayGame():
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    screenW = 1280
    screenH = 720

    clock = pygame.time.Clock()
    running = True
    dt = 0
    ball_pos = Vec2(screenW / 2, screenH / 2)
    ball_dir = Vec2(300, 300)
    player_pos = Vec2(30, 30)
    globScore = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #User input 
        direction = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            direction = 1
        if keys[pygame.K_s]:
            direction = -1


        drawObjects(screen, player_pos, ball_pos, globScore, -1, -1)
        player_pos = gameMovement(screenW, screenH, direction, player_pos, dt)
        ball_pos, running, globScore = ballMovement(screenW, screenH, dt, ball_dir, ball_pos, player_pos, running, globScore)
        
        # limits FPS to 1200
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(1200) / 1000 #Around 0.001
    
    pygame.quit()
    return(globScore)

def AIControlled(screenW, screenH, player_pos, ball_pos, ball_dir, running, globScore, direction, trainieNum = -1, genNum = -1, visual = True, screen = None, clock = None):
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    if visual:
        dt = clock.tick(2400) / 100 #First number is framerate, second controls actual speed
        drawObjects(screen, player_pos, ball_pos, globScore, trainieNum, genNum) #Function to draw shapes and text
    else:
        dt = 0.01
    player_pos = gameMovement(screenW, screenH, direction, player_pos, dt) #Movies the player and ensures it maintains within the bounds
    ball_pos, running, globScore = ballMovement(screenW, screenH, dt, ball_dir, ball_pos, player_pos, running, globScore) #Moves the ball and checks it's collisions
        
    array = [player_pos.x / 100, player_pos.y / 100, ball_pos.x / 100, ball_pos.y / 100, ball_dir.x / 100, ball_dir.y / 100] #Array to hold the values that the network uses. It is divided by 100 because it overflows in the sigmoid function
    return(array, running, globScore, player_pos, ball_pos, ball_dir) #Returning the updated infomation


if __name__ == '__main__':
    displayGame() #Player controlled game
