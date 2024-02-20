import math
import pygame
  
pygame.init()
size = (400,400)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

def blitRotate(image, pos, originPos, angle):
    image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    rotated_offset = offset_center_to_pivot.rotate(-angle)
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
    rotated_image.set_colorkey((255, 255, 255))

    return rotated_image, rotated_image_rect

def generate_rotate_cache(image, pivot, interval=1, scale=4):
    cache = {}
    for i in range(361):
        cache[i] = blitRotate(image, (0,0), pivot, i)

    return cache

image = pygame.image.load("sword_1.png").convert_alpha()
image = pygame.transform.scale_by(image, 3)
image.set_colorkey((255, 255, 255))


rect = image.get_rect()
pivot = rect.bottomleft

cache = generate_rotate_cache(image, rect.bottomleft)


angle, frame = 0, 0
done = False
while not done:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill(0)

    pos = pygame.mouse.get_pos()
    #(200 + math.cos(frame * 0.05)*100, 200 + math.sin(frame * 0.05)*50)

    img = cache[angle]
    screen.blit(img[0], pos)

    pygame.draw.line(screen, (0, 255, 0), (pos[0]-20, pos[1]), (pos[0]+20, pos[1]), 3)
    pygame.draw.line(screen, (0, 255, 0), (pos[0], pos[1]-20), (pos[0], pos[1]+20), 3)
    pygame.draw.circle(screen, (0, 255, 0), pos, 7, 0)

    pygame.display.flip()
    frame += 1
    angle += 1
    angle %= 360
    
pygame.quit()
exit()