import pygame, sys
from PIL import Image

WIDTH, HEIGHT = 800,600
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.Clock()

def prep_image(img, scale, colorkey=(255,255,255)):
      rect = img.get_rect()
      img = pygame.transform.scale_by(img, scale)
      img.set_colorkey(colorkey)
      return img

def prep_image2(path, scale, colorkey=(255,255,255)):
    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.scale_by(img, scale)
    img.set_colorkey(colorkey)

    return img

def get_images(spritesheet):
    SECTION_START = (255,0,255)
    SECTION_END = (63,72,204)

    start = []
    end = []

    spritesheet = spritesheet.convert("RGB")
    
    width, height = spritesheet.size
    for x in range(width):
        for y in range(height):
            c = spritesheet.getpixel((x, y))
            if c == SECTION_START:
                start.append([x,y])
            elif c == SECTION_END:
                end.append([x,y])

    images = []
    for i in range(len(start)):
        img = spritesheet.crop([start[i][0]+1, start[i][1]+1, end[i][0], end[i][1]])
        image_bytes = img.tobytes()

# Create a Pygame surface from the bytes object
        img2 = pygame.image.fromstring(image_bytes, img.size, 'RGB')#.set_colorkey((255,255,255))
        images.append(img2)

    return images

spritesheet = Image.open("knight4.png")
images = get_images(spritesheet)
images = [prep_image(image, 8) for image in images]


i = 0
while True:
    clock.tick(12)
    i += 1
    screen.fill((0,30,0))
    screen.blit(images[i%5], (100,100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            pygame.quit()

    pygame.display.update()