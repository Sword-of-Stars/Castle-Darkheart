import pygame, sys
import math, random
from PIL import Image

#from scripts.entities.entity import Entity

WIDTH, HEIGHT = 800,600

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def spiral_attack(t, pos, rate):
    speed = 4 # how often projectiles fire
    k = 3 # number of projectiles fired at a time

    if t%speed == 0:
        for i in range(k):
            pass # create a projectile

class Entity(pygame.sprite.Sprite):
    def __init__(self, speed, layer=0):
        pygame.sprite.Sprite.__init__(self)

        self.vel = pygame.Vector2(0,0)
        self.speed = speed
        self.MAXSPEED = speed
        self.layer = layer

class Razak(Entity):
    def __init__(self, pos):
        Entity.__init__(self, 0, 2)

        self.images = [prep_image(x, 4) for x in get_images("data/wraith_exp.png")]
        self.body = self.images[1]
        self.rect = self.body.get_rect()
        self.rect.center = pos
        self.pos = pos

        self.hands = (self.images[0], self.images[2])
        self.hand_rect = self.hands[0].get_rect()
        self.hand_positions = [[],[]]

        self.all_spells = self.images[3:]
        self.spells = self.repopulate_spells()
        self.state = "idle"
        
        self.attack_timer_max = 60
        self.attack_timer = self.attack_timer_max
        self.active_spell = None

        self.glow = prep_image(pygame.image.load("data/radial_gradient.png"), 1)

        self.t = 0

    def repopulate_spells(self):
        spells = {
            "spiral":
                {
                "img":self.all_spells[0], 
                "duration":120,
                "function":0
                },
            "homing":
                {
                "img":self.all_spells[1], 
                "duration":120,
                "function":0
                },
            "linear":
                {
                "img":self.all_spells[2], 
                "duration":120,
                "function":0
                },
            "summon":
                {
                "img":self.all_spells[3], 
                "duration":120,
                "function":0
                },
            "shotgun":
                {
                "img":self.all_spells[4], 
                "duration":120,
                "function":0
                }
            }
        return spells


    def update_hands(self):
        for i, hand in enumerate(self.hands):
            k = 45
            if i == 1:
                x_offset = -k
                y_off = 0.3
            else:
                x_offset = k-self.hand_rect.width
                y_off = 0
            
            self.hand_positions[i] =  [self.rect.centerx + x_offset,
                               self.rect.centery+5*math.sin(self.t+y_off)+10]
            
    def draw_hands(self):
        screen.blit(self.hands[0], self.hand_positions[0])
        screen.blit(self.hands[1], self.hand_positions[1])
           
    def draw_spells(self):
        if len(self.spells) > 0:
            delta = 2*math.pi/len(self.spells)

            for i, spell in enumerate(self.spells):
                screen.blit(self.spells[spell]["img"], (-10+self.rect.centerx + 45*math.cos(self.t+(delta*i)),
                                    20+self.rect.centery + 25*math.sin(self.t+(delta*i))))
    
    def draw_body(self):
        screen.blit(self.body, self.rect)

    def attack(self):
        if self.state != "attack":
            self.state = "attack"
            self.attack_timer = self.attack_timer_max

            self.active_spell = None
            if len(self.spells) > 0:
                self.active_spell = self.spells.pop(random.choice(list(self.spells.keys())))

        else:
            self.attack_timer -= 1
            y_off = -50
            self.hand_positions[0][1] = self.rect.centery + y_off
            self.hand_positions[1][1] = self.rect.centery + y_off

            if self.active_spell != None:
                screen.blit(self.active_spell["img"], (self.rect.centerx-10, self.rect.top-40))

        if self.attack_timer <= 0:
            self.state = "idle"


    def idle(self):
        self.pos[1] += 1*math.cos(self.t)

    def draw(self):
        pass


    def update(self):
        self.t = self.t+0.1%math.pi

        self.update_hands()

        if self.state == "idle":
            self.idle()
        elif self.state == "attack":
            self.attack()

        self.rect.center = self.pos

        self.draw_hands()
        self.draw_spells()
        self.draw_body()

        


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

razak = Razak([WIDTH//2, HEIGHT//2])

while True:
    clock.tick(60)
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                razak.attack()

    razak.update()

    pygame.display.flip()