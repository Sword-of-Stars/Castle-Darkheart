import pygame, sys
import math

from PIL import Image

WIDTH, HEIGHT = 800, 600

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def prep_image(img, scale, colorkey=(255,255,255)):
    """
    Given an image, sets scale and colorkey

    Args:
        img (pygame.Surface): image to be prepped
        scale (seq OR int): scale factor
        colorkey (seq): image colorkey
    Returns:
        img (pygame.Surface): the prepared image
    """

    img = pygame.transform.scale_by(img, scale)
    img.set_colorkey(colorkey)
    img = img.convert_alpha()

    return img

def get_images(spritesheet_loc):
    """Extracts a series of images from a spritesheet

    Args:
        spritesheet_loc (str): location of the spritesheet

    Returns:
        list: a list of images
    """

    # RGB values for corner pieces
    SECTION_START = (63,72,204)
    SECTION_END = (255,174,201)

    start = []
    end = []

    with Image.open(spritesheet_loc) as spritesheet:
        
        # Get dimensions of spritesheet
        width, height = spritesheet.size

        # Side effect of removing transparency
        spritesheet = spritesheet.convert("RGB")

        # Loop through every pixel in sheet (top to bottom, left to right)
        for x in range(width):
            for y in range(height):

                # Get the pixel value and see if it's important
                c = spritesheet.getpixel((x, y))
                if c == SECTION_START:
                    start.append([x,y])
                elif c == SECTION_END:
                    end.append([x,y])

        images = []

        # For each detected image, 
        for i in range(len(start)):

            # Isolates the desired image chunk
            img = spritesheet.crop([start[i][0]+1, start[i][1]+1, end[i][0], end[i][1]])
            image_bytes = img.tobytes()

            # Create a Pygame surface from the bytes object
            img2 = pygame.image.fromstring(image_bytes, img.size, 'RGB')
            images.append(img2)

        return images

images = [prep_image(x, 4) for x in get_images("data/spirit_02.png")]

class Dancer:
    def __init__(self, center, angle, length, k):
        self.pos = center
        self.center = center
        self.angle = angle
        self.length = length
        self.k = k

        self.frames = images
        self.frame = 0
        self.fps = 0.2

        self.rect = self.frames[0].get_rect()

        self.x_flip = False
        self.prev_x = 0

    def update(self, t):
        self.angle = (self.angle + dt) % (2 * math.pi)
        x = self.length * math.sin(self.k * t) * math.cos(self.angle)
        y = self.length * math.sin(self.k * t) * math.sin(self.angle)

        self.x_flip = self.prev_x > x
        self.prev_x = x

        self.pos = [self.center[0] + x - self.rect.width/2, self.center[1] + y - self.rect.height/2]

    def draw(self):
        self.frame = (self.frame +self.fps)% len(self.frames)
        img = pygame.transform.flip(self.frames[int(self.frame)], self.x_flip, False)
        screen.blit(img, self.pos)

def generate_rose(length, k, center):

    dancers = []
    for i in range(0, k):
        dancer = Dancer(
            center=[center[0] + math.cos(2 * math.pi / k * i) * length, center[1] + math.sin(2 * math.pi / k * i) * length],
            angle=2*math.pi / k * i,
            length=length,
            k=k
        )
        dancers.append(dancer)
    return dancers

dancers = generate_rose(150, 9, [WIDTH // 2, HEIGHT // 2])

dt = .01
t = 0

while True:
    clock.tick(60)
    screen.fill((0, 0, 0))

    t += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update dancers
    for dancer in dancers:
        dancer.update(t)

    pygame.draw.circle(screen, (255, 0, 0), [WIDTH // 2, HEIGHT // 2], 10)

    for dancer in dancers:
        dancer.draw()

    pygame.display.flip()
