import pygame, sys
import math

from PIL import Image

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.init()

# Functions

def get_images(spritesheet):
    SECTION_START = (255,0,255)
    SECTION_END = (63,72,204)

    start = []
    end = []
    
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

def angle_to(e1, e2):
    dx = e2[0]-e1[0]
    dy = e2[1]-e1[1]
    return math.degrees(math.atan2(dy,dx))

def blitRotateCenter(surf, image, topleft, angle):

    rotated_image = pygame.transform.rotozoom(image, angle, 1)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = topleft).center)

    surf.blit(rotated_image, new_rect)

def draw_circle(frame):
    subsurf = pygame.surface.Surface((80,40))
    subsurf.fill((0,0,0))
    pygame.draw.circle(subsurf, (255, 255, 255), (20,20), 20)
    pygame.draw.circle(subsurf, (0,0,0), (32,20), 20)
    subsurf = pygame.transform.scale_by(subsurf, (4,2)) # ALl I need to do is come up with some fancy maths
        # To offset the scaling in a trigonometric way and voila!, it is completed. 
    subsurf.set_colorkey((0,0,0))
    #subsurf = pygame.transform.rotozoom(subsurf, frame, 1)
    subsurf = pygame.transform.rotate(subsurf, frame)
    #subsurf = pygame.transform.scale_by()
    
    blitRotateCenter(screen, subsurf, (100,100), frame)

def draw_circle_2(angle, img, pos):
    blitRotateCenter(screen, img, pos, angle)

def prep_smears():
    with Image.open("smears.png") as img:
        smears = get_images(img)

    smears = [pygame.transform.scale_by(x, (3,2)) for x in smears]
    for x in smears:
        x.set_colorkey((0,0,0))

    return smears

class Player():
    def __init__(self):
        self.pos = (WIDTH//2, HEIGHT//2)
        self.color = (0,0,255)
        self.radius = 30

        self.smear_frames = prep_smears()

    def update(self):
        pygame.draw.circle(screen, self.color, self.pos, self.radius)

player = Player()
surf = draw_circle(0)

min_fps = 10000
avg_fps = 0
frame = 0


smear_frame = 0

while True:
    smear_frame += 0.2
    frame += 1
    clock.tick(60)
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    player.update()

    fps = clock.get_fps()
    avg_fps += fps
    if fps < min_fps and fps != 0:
        min_fps = fps

    pos = pygame.mouse.get_pos()
    pygame.draw.circle(screen, (255, 0,0), pos, 10)

    angle = int(angle_to(pos, player.pos))

    pygame.display.set_caption(f"min: {min_fps}, avg: {avg_fps/frame}")

    draw_circle_2(-angle, player.smear_frames[int(smear_frame)%len(player.smear_frames)], pos)

    pygame.display.update()