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
# NICE! I implemented some cosmetics, isolated the animation from the sword, 
# and overall improved the quality of the code

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
   
    return angle

def blitRotateCenter(surf, image, topleft, angle):
    """
    Rotates an image about its center. 
    This is a faster method for its specific use case. For rotating about an 
    arbitrary pivot point, use the more generic function 'blitRotate'
    """
    rotated_image = pygame.transform.rotozoom(image, angle, 1)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = topleft).center)

    surf.blit(rotated_image.convert_alpha(), new_rect)

def blitRotate(surf, image, pos, originPos, angle):
    """
    Rotates an image about an arbitrary pivot point. 
    The pivot is given as 'originPos,' and the math is performed through 
    vector rotations
    """
    image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    rotated_offset = offset_center_to_pivot.rotate(-angle)
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
    
    surf.blit(rotated_image.convert_alpha(), rotated_image_rect)

# Objects
class Player():
    def __init__(self):
        self.pos = (WIDTH//2, HEIGHT//2)
        self.color = (0,0,255)
        self.radius = 30

        self.img = pygame.image.load("player.png").convert_alpha()
        self.img = pygame.transform.scale_by(self.img, 2.7)
        self.img.set_colorkey((255,255,255))
        
        self.rect = self.img.get_rect(center = self.pos)

        self.sword = Sword(self)

    def update(self, pos):
        #pygame.draw.circle(screen, self.color, self.pos, self.radius)

        img = pygame.transform.flip(self.img, (pos[0] < WIDTH//2), False)
        img.set_colorkey((255,255,255))

        if self.sword.render_over():
            screen.blit(img, self.rect.topleft)
            self.sword.update(pos)
        else:
            self.sword.update(pos)
            screen.blit(img, self.rect.topleft)

class Weapon():
    def _init__(self):
        pass

class Sword(Weapon):
    def __init__(self, player):
        Weapon.__init__(self)
        self.player = player

        # Load sword image and smear images
        self.load_sword_image()
        self.load_smear_images()

        # Swing Angular Information
        self.angle = 0 # The actual angle of the sword
        self.initial_angle = 135 # Sword initially drawn at 45 degree angle
        self.angle_relative_to_target = 120 # Angle of the sword hilt relative to the target

        self.side = -1 # -1 for left/ccw, 1 for right/cw
        self.length = 60 # Distance from player
        self.pos = self.set_pos(0, self.length)

        # Physics attributes
        self.physics_stop = 120
        self.physics_decay = 1.5
        self.angular_velocity = 0

        self.is_swing = False # is the player currently swinging?
        self.num_cooldown_frames = 8
        self.current_swing_frame = 0

       # Initialize the smear attributes
        self.active_smear = False
        self.smear_animations = []
        self.smear_frame = 0
        self.smear_frames = len(self.smears)
        self.smear_angle = 0
        self.frame_rate = 1/3

        self.smear_length = 110 # distance from player to smear
        self.smear_pos = self.set_pos(90, self.smear_length)


    def load_sword_image(self):
        self.img = pygame.transform.scale_by(pygame.image.load("sword_1.png").convert_alpha(), 4)
        self.img.set_colorkey((255,255,255))
        self.rect = self.img.get_rect()

    def load_smear_images(self):
        with Image.open("smears_2.png") as img:
            self.smears = get_images(img)
        self.smears = [pygame.transform.scale_by(x, (3,4)) for x in self.smears]
        for x in self.smears:
            x.set_colorkey((0,0,0))

    def render_over(self):
        """
        This function determines whether to draw the function on top of
        or below the player
        """
        angle = angle_to(self.player.pos, self.player.sword.pos)

        if self.side == -1:
            if angle < 140 and angle > -40:
                return True # Sword on top
            return False
        else:
            if angle < 20 and angle > -160:
                return False # Sword on bottom
            return True

    def set_angle(self, pos):

        angle = angle_to(self.player.pos, pos)
        a = angle + self.angle_relative_to_target*self.side

        if not self.is_swing:
            self.pos = self.set_pos(a, self.length)
        else:
            self.pos = self.set_pos(a+self.angular_velocity*self.side, self.length)
            
        self.smear_pos = self.set_pos(angle, -self.smear_length)

        self.angle = self.initial_angle - angle 
        self.smear_angle = 180 - angle

    def set_pos(self, angle, length):
        return (self.player.pos[0]-length*math.cos(math.radians(angle)), 
                self.player.pos[1]-length*math.sin(math.radians(angle)))

    def swing(self):
        if not self.is_swing:
            self.is_swing = True
            self.active_smear = True
            self.smear_frame = 0
            self.side *= -1

            self.smear_animations.append(Animation(self.smears, self.frame_rate, 
                                                   self.smear_pos, self.smear_angle))
    
    def reset_swing(self):
        self.physics_stop = 80
        self.current_swing_frame = 0
        self.is_swing = False

    def handle_swing(self):

        if self.current_swing_frame <= (self.num_cooldown_frames):
            # If the sword is NOT done swinging
            self.angle -= self.physics_stop*self.side
            self.physics_stop /= self.physics_decay
        else:
            self.reset_swing()

        self.current_swing_frame += 1
           
    def handle_smear(self):

        for smear in reversed(self.smear_animations):
            if smear.alive:
                smear.update()
            else:
                self.smear_animations.remove(smear)

    def draw_sword(self):
        blitRotate(screen, self.img, self.pos, self.rect.bottomleft, self.angle)

    def update(self, pos):
        self.set_angle(pos)

        if self.is_swing:
            self.handle_swing()

        self.handle_smear()
        self.draw_sword()

class Animation():
    def __init__(self, frames, framerate, pos, angle, static=True):
        self.frames = frames
        self.num_frames = len(frames)
        self.frame = 0
        self.framerate = framerate
        self.pos = pos
        self.angle = angle

        self.alive = True

    def update(self):
        if self.frame >= self.num_frames:
            self.alive = False
        else:
            blitRotateCenter(screen, self.frames[int(self.frame)%self.num_frames], self.pos, self.angle)
            self.frame += self.framerate

player = Player()

while True:
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
    player.update(pos)

    pygame.display.update()