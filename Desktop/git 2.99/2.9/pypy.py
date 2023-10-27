import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
window = pygame.display.set_mode((1280, 720), pygame.SCALED)
pygame.display.set_caption('Pygame SCALED Example')

# Initial position of the rectangle
x, y = 50, 50

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Handle key events to move the rectangle
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        x -= 5
    if keys[pygame.K_RIGHT]:
        x += 5
    if keys[pygame.K_UP]:
        y -= 5
    if keys[pygame.K_DOWN]:
        y += 5

    # Draw
    window.fill((0, 0, 0))  # Fill the screen with black
    pygame.draw.rect(window, (255, 0, 0), (x, y, 50, 50))  # Draw a red rectangle

    pygame.display.update()  # Update the display
