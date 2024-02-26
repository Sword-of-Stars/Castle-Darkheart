import pygame, sys
from PIL import Image

pygame.init()
WIDTH, HEIGHT = 800,600

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
frame = 0
fps = 0.1

while True:
    clock.tick(60)
    screen.fill((0,0,0))

    frame = (frame+fps)%len(images)

    screen.blit(images[int(frame)], (100,100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.flip()