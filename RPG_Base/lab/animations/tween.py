import pygame
import pytweening

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()

# Set screen dimensions
WIDTH, HEIGHT = 800,600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

rect = pygame.Rect(100, HEIGHT//2, 100,100)

# Create a tween to move the sprite horizontally
t = 0

running = True
while running:
    clock.tick(60)
    t += 0.01
    t = t % 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the tween
    rect.x = 100+pytweening.easeInOutBack(t, 1000)
    #print(pytweening.easeOutBounce(t))
    # Draw the sprite
    screen.fill((255, 255, 255))  # Clear the screen
    pygame.draw.rect(screen, (255, 0, 0), rect, 50)

    # Update the display
    pygame.display.update()

pygame.quit()
