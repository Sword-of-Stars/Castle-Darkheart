import pygame
import math

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sword Swing")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load sword image and get its rect
sword_img = pygame.image.load("sword_1.png")
sword_rect = sword_img.get_rect(x=100,y=100)
sword_pivot = (sword_rect.width // 2, 0)  # Assuming the pivot point is at the top-center of the sword

# Initialize sword angle and rotation variables
sword_angle = 0
rotation_speed = 5

clock = pygame.time.Clock()

def swing_sword(angle):
    rotated_sword = pygame.transform.rotate(sword_img, angle)
    new_rect = rotated_sword.get_rect(center=sword_rect.center)
    return rotated_sword, new_rect

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Start sword swing on mouse click
            sword_angle = 0

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False

    # Calculate the angle between the sword pivot and the mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dx, dy = mouse_x - sword_rect.centerx, mouse_y - sword_rect.centery
    target_angle = math.degrees(math.atan2(dy, dx))

    # Smoothly rotate the sword towards the target angle
    d_angle = (target_angle - sword_angle) % 360
    if d_angle > 180:
        d_angle -= 360
    if d_angle < -180:
        d_angle += 360

    if abs(d_angle) > rotation_speed:
        rotation_direction = 1 if d_angle > 0 else -1
        sword_angle += rotation_direction * rotation_speed
    else:
        sword_angle = target_angle

    screen.fill(WHITE)

    # Rotate and display the sword
    rotated_sword, rotated_rect = swing_sword(sword_angle)
    screen.blit(rotated_sword, rotated_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
