import pygame, sys
import math
import pytweening

from PIL import Image

# NOTE: This is sh*t spaghetti code
# NOTE: Now, this is slightly less sh*t code, so I'm happier. However, I'd need to 
# tidy up how it all works and fix my opposite directional offset IOT finally fix this 
# annoying mechanic. Once complete, I'd also like to try and optimize it, but this 
# may be unnecessary
# NOTE: Problem is, currently swinging is tied to the frames

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
    angle = math.degrees(math.atan2(dy,dx))
    #if angle < 0:
        #angle += 360
    return angle

def blitRotateCenter(surf, image, topleft, angle):

    rotated_image = pygame.transform.rotozoom(image, angle, 1)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = topleft).center)

    surf.blit(rotated_image.convert_alpha(), new_rect)

def blitRotateCenter_2(surf, image, topleft, angle):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = topleft).center)
    rotated_image.set_colorkey((255,255,255))

    surf.blit(rotated_image.convert_alpha(), new_rect)

def draw_circle_2(angle, img, pos):
    blitRotateCenter(screen, img, pos, angle)

def fps_tracker(avg_fps, min_fps):
    fps = clock.get_fps()
    avg_fps += fps
    if fps < min_fps and fps != 0:
        min_fps = fps
    return avg_fps, min_fps

# Objects
class Player():
    def __init__(self):
        self.pos = (WIDTH//2, HEIGHT//2)
        self.color = (0,0,255)
        self.radius = 30

        self.sword = Sword(self)

    def update(self, pos):
        pygame.draw.circle(screen, self.color, self.pos, self.radius)
        self.sword.update(pos)

class Sword():
    def __init__(self, player):
        self.player = player

        # Load sword image and smear images
        self.load_sword_image()
        self.load_smear_images()

        self.active_smear = False
        self.smear_frame = 0
        self.smear_frames = len(self.smears)
        self.frame_rate = 0.33
        

        # Swing-related information
        self.angle = 0
        self.initial_angle = 45

        self.side = -1 # -1 for left, 1 for right
        self.flip = False

        self.is_swing = False
        self.half_delta = 90

        self.current_swing_frame = 1
        self.num_swing_frames = 2

        self.angular_velocity = 0
        self.smear_angle = 0
        self.swing_dir = -1 # -1 is counterclockwise, 1 is clockwise

        # Misc
        self.length = 80 # Distance from player
        self.smear_length = 180
        self.pos = self.set_pos(0, self.length)
        self.smear_pos = self.set_pos(90, self.smear_length) #broken

    def load_sword_image(self):
        self.img = pygame.transform.scale_by(pygame.image.load("sword_2.png").convert_alpha(), 4)
        self.img.set_colorkey((255,255,255))

    def load_smear_images(self):
        with Image.open("smears_2.png") as img:
            self.smears = get_images(img)
        self.smears = [pygame.transform.scale_by(x, (3,4)) for x in self.smears]
        for x in self.smears:
            x.set_colorkey((0,0,0))

    def set_angle(self, pos):
        angle = angle_to(self.player.pos, pos)

        a = angle + self.half_delta*self.side

        if not self.is_swing:
            self.set_pos(a, self.length)
        else:
            self.set_pos(a+self.angular_velocity*self.current_swing_frame*self.swing_dir, self.length)
            
        self.smear_pos = (self.player.pos[0]+self.smear_length*math.cos(math.radians(angle)), 
                        self.player.pos[1]+self.smear_length*math.sin(math.radians(angle)))

        self.angle = -angle + self.initial_angle + 90
        self.smear_angle = -angle + 180

    def set_pos(self, angle, length):
        self.pos = (self.player.pos[0]-length*math.cos(math.radians(angle)), 
                    self.player.pos[1]-length*math.sin(math.radians(angle)))

    def swing(self):
        self.is_swing = True
        self.active_smear = True
        self.smear_frame = 0

    def handle_swing(self):
        if self.current_swing_frame != self.num_swing_frames:
            self.angular_velocity = 2*self.half_delta/self.num_swing_frames
            self.angle -= 2*self.angular_velocity*self.current_swing_frame*self.swing_dir

            self.current_swing_frame += 1



        if self.current_swing_frame == self.num_swing_frames:
            self.is_swing = False
            self.side *= -1
            self.swing_dir*=-1
            self.current_swing_frame = 1
        


    def handle_smear(self):
        self.smear_frame += self.frame_rate

        if int(self.smear_frame) == self.smear_frames:
            self.active_smear = False
        else:
            blitRotateCenter(screen, self.smears[int(self.smear_frame)%self.smear_frames], self.smear_pos, self.smear_angle)






    def update(self, pos):
        self.set_angle(pos)

        if self.is_swing:
            self.handle_swing()
        if self.active_smear:
            self.handle_smear()
       
        blitRotateCenter_2(screen, self.img, self.pos, self.angle)

        pygame.draw.circle(screen, (0,255,0), self.pos, 10)


player = Player()

min_fps = 10000
avg_fps = 0
frame = 0

length = 80

while True:
    frame += 1
    clock.tick(60)
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            player.sword.swing()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass

    pos = pygame.mouse.get_pos()
    angle = int(angle_to(player.pos, pos))
  
    sword_pos = (player.pos[0]+length*math.cos(math.radians(angle)), player.pos[1]+length*math.sin(math.radians(angle)))
    pygame.draw.circle(screen, (255, 0, 0), sword_pos, 20)

   
    avg_fps, min_fps = fps_tracker(avg_fps, min_fps)
    pygame.display.set_caption(f"min: {min_fps}, avg: {avg_fps/frame}")


    player.update(pos)

    pygame.display.update()