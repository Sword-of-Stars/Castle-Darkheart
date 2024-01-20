import pygame, sys

WIDTH, HEIGHT = 500,500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

my_img = pygame.image.load("sword_1.png").convert_alpha()
my_img = pygame.transform.scale_by(my_img, 3)
my_img.set_colorkey((255, 255, 255))

temp_rect = my_img.get_rect()
offset = pygame.Vector2(temp_rect.center) - pygame.Vector2(temp_rect.bottomleft)

angle = 0

def rotate(surface, angle, pivot, offset):
    """Rotate the surface around the pivot point.

    Args:
        surface (pygame.Surface): The surface that is to be rotated.
        angle (float): Rotate by this angle.
        pivot (tuple, list, pygame.math.Vector2): The pivot point.
        offset (pygame.math.Vector2): This vector is added to the pivot.
    """
    rotated_image = pygame.transform.rotozoom(surface, -angle, 1)  # Rotate the image.
    rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
    # Add the offset vector to the center/pivot point to shift the rect.
    rect = rotated_image.get_rect(center=pivot+rotated_offset)
    return rotated_image, rect  # Return the rotated image and shifted rect.

while True:
    clock.tick(60)
    screen.fill((0,0,0))

    angle += 1
    angle %= 360

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pos = pygame.mouse.get_pos()

    rotated_image, rect = rotate(my_img, angle, pos, pygame.Vector2((0,0)))
    screen.blit(rotated_image, (pos))

    pygame.display.update()
