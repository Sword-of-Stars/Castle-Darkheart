import pygame, sys
import math
from PIL import Image
import pytweening

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


images = [prep_image(x, 4) for x in get_images("data/wendigo_exp.png")]
print(len(images))
body = images[2]
razak_rect = body.get_rect(x = 100, y=100)
hands = (images[0], images[1])
hand_rect = hands[0].get_rect()

t = 0

img = pygame.image.load("data/radial_gradient.png")
glow = prep_image(img, 1)

left_hand_pos = razak_rect.center

attack = False

attack_reach = 60
attack_curve = [12, 5, 10, 22] # windup, approach, impact, recede
attack_timer_max = sum(attack_curve)
attack_timer = attack_timer_max

def angle_to(e1, e2):
    """Returns the angle from e1 to e2

    Arg:
        e1, e2 (seq): x-y coordinates
    Returns:
        float: angle in degrees
    """

    dx = e2[0]-e1[0]
    dy = e2[1]-e1[1]
    angle = math.degrees(math.atan2(dy,dx))
   
    return angle

def distance(e1, e2):
    dx = e2[0]-e1[0]
    dy = e2[1]-e1[1]
    return math.hypot(dx, dy)

while True:
    clock.tick(60)
    screen.fill((255, 255, 255))

    t = t+0.1%math.pi

    pos = pygame.mouse.get_pos()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if attack == False:
                    attack = True
                    attack_timer = attack_timer_max
                    attack_target = pos
                    attack_reach = 100

      
    if attack_timer > 0:
        attack_timer -= 1
    elif attack_timer == 0:
        attack = False
    
    screen.blit(body, razak_rect)

    if not attack:
        left_hand_pos = [razak_rect.centerx - 70, razak_rect.centery + math.cos(t)*4 + 30]
        screen.blit(hands[0], left_hand_pos)

        right_hand_pos = [razak_rect.centerx + 70-hand_rect.width, razak_rect.centery + math.cos(t-1)*4 + 30]
        screen.blit(hands[1], right_hand_pos)

        razak_rect.y = HEIGHT//4+10*math.cos(t)


    elif attack:
        windup = 100

        if attack_timer >= attack_timer_max-attack_curve[0]: # in the approach phase
            ti = min(1, 1-2*(attack_timer - (attack_timer_max-attack_curve[0]))/(attack_timer_max-attack_curve[0]))
            left = left_hand_pos[1] - pytweening.easeInOutQuad(ti)*windup
            print(ti)

        elif attack_timer >= attack_timer_max-sum(attack_curve[:2]): # in the approach phase
            pass

        elif attack_timer >= attack_timer_max-sum(attack_curve[:3]): # in the approach phase
            left = left_hand_pos[1]+20

        else: # in the approach phase
            pass
      
        screen.blit(hands[0], (left_hand_pos[0], left))

        #right_hand_pos = [razak_rect.centerx + 70-hand_rect.width, razak_rect.centery + math.cos(t-1)*4 + 30]
        screen.blit(hands[1],  (right_hand_pos[0], left-5))

        razak_rect.y = HEIGHT//4+3*math.cos(t)


            

    pygame.display.flip()