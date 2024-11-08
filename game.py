# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
ball_dir = pygame.Vector2(1, 1)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    pygame.draw.rect(screen, "white", pygame.Rect(screen.get_width() - 30, 0, 60, screen.get_height()))
    pygame.draw.rect(screen, "white", pygame.Rect(0, 0, screen.get_width() - 30, 30))
    pygame.draw.rect(screen, "white", pygame.Rect(0, screen.get_height() - 30, screen.get_width(), 30))

    pygame.draw.circle(screen, "red", player_pos, 40)

    #Player

    # Moving ball
    player_pos.y += ball_dir.y * dt
    player_pos.x += ball_dir.x * dt

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()