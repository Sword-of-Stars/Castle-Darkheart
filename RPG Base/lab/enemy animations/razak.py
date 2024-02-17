import pygame, sys
import math
from PIL import Image

WIDTH, HEIGHT = 800,600

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


images = [prep_image(x, 4) for x in get_images("data/wraith_exp.png")]
print(len(images))
razak = images[1]
razak_rect = razak.get_rect(x = WIDTH//2, y=HEIGHT//2)
hands = (images[0], images[2])
hand_rect = hands[0].get_rect()

spells = images[3:]

t = 0

img = pygame.image.load("data/radial_gradient.png")
glow = prep_image(img, 1)

while True:
    clock.tick(60)
    screen.fill((255, 255, 255))

    t = t+0.1%math.pi

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                spells.pop()

    razak_rect.y = HEIGHT//2+10*math.cos(t)

    for i, hand in enumerate(hands):
        k = 45
        if i == 1:
            x_offset = -k
            y_off = 0.3
        else:
            x_offset = k-hand_rect.width
            y_off = 0
        screen.blit(hand, (razak_rect.centerx + x_offset,razak_rect.centery+5*math.sin(t+y_off)+10))

    delta = 2*math.pi/len(spells)
    undrawn = []

    for i, spell in enumerate(spells):
        #if 25*math.sin(t+(delta*i)) < 0:
        #screen.blit(glow, (-20+razak_rect.centerx + 45*math.cos(t+(delta*i)), 10+razak_rect.centery + 25*math.sin(t+(delta*i))))

        screen.blit(spell, (-10+razak_rect.centerx + 45*math.cos(t+(delta*i)), 20+razak_rect.centery + 25*math.sin(t+(delta*i))))
        #else:
            #ndrawn.append((i, spell))

    screen.blit(razak, razak_rect)


    #for i, spell in undrawn:
        #if math.sin(t+(delta*i)) < 0:
            #screen.blit(spell, (razak_rect.centerx + 45*math.cos(t+(delta*i)), razak_rect.centery + 25*math.sin(t+(delta*i))))





    pygame.display.flip()