import pygame, sys
import math

pygame.init()
WIDTH, HEIGHT = 400,400
screen_center = (WIDTH/2, HEIGHT/2)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Mostly working, just a weird visual bug at certain angles. Fixable, just annoying (6-1-23)

def bound_angle(angle):
    while angle < 0:
        angle += 360
    while angle > 360:
        angle -= 360
    return angle

def load_pixel_image(file_name, colorkey=(255,255,255), scale=4):
    img = pygame.image.load(file_name).convert_alpha()
    img.set_colorkey(colorkey)
    img = pygame.transform.scale(img, [x*scale for x in img.get_size()]).convert_alpha()
    return img

class Sword(pygame.sprite.Sprite):
    def __init__(self):
        self.angle = 0
        self.swing_angle = 0
        self.distance_from_body = 100
        self.normal_distance_from_body = 100
        self.swing_distance_from_body = 80

        self.image = load_pixel_image("data/sword_2.png")
        self.smear_1 = load_pixel_image("data/smear_6.png")
        self.smear_2 = load_pixel_image("data/smear_8.png")


        self.extended_swing = False

        self.smear = self.smear_1
        self.smear_pos = (0,0)
        self.smear_angle = self.angle

        self.rect = self.image.get_rect()
        self.width, self.height = self.rect[2], self.rect[3]
        self.center_x, self.center_y = self.rect[2]/2, self.rect[3]/2

        self.state = 'idle'
        self.side = 'left'
        self.swing_cooldown = 0
        self.MAX_SWING_COOLDOWN = 10
        self.angle_relative_to_body = 0
        self.swing_angle_change = 60
        self.swing_angle_corrective_factor = 80

    def handle_cooldown(self):
        if self.swing_cooldown > 0:
            self.swing_cooldown -= 1
        if self.swing_cooldown <= 0:
            self.state = 'idle'
            self.distance_from_body = self.normal_distance_from_body

    def swing(self):
        if self.swing_cooldown <= 0:
            self.state = 'swing'
            self.swing_cooldown = self.MAX_SWING_COOLDOWN
            self.distance_from_body = self.swing_distance_from_body

            if self.side == 'right':
                self.extended_swing = False
                self.swing_angle = self.angle_relative_to_body + self.swing_angle_change
                if self.swing_angle > 270 and self.swing_angle < 280:
                    self.extended_swing = True
                elif self.swing_angle > 270:
                    self.swing_angle -= 10

                if not self.extended_swing:
                    img = pygame.transform.rotate(self.smear_1, 90)
                    self.smear = pygame.transform.flip(img, True, False)
                else:
                    img = pygame.transform.rotate(self.smear_2, 90)
                    self.smear = pygame.transform.flip(img, True, False)

            else:
                self.swing_angle = self.angle_relative_to_body - self.swing_angle_change

                self.extended_swing = False
                if self.swing_angle > 260 and self.swing_angle < 270:
                    self.extended_swing = True
                elif self.swing_angle < 270 and self.swing_angle > 90:
                    self.swing_angle += 10

                if not self.extended_swing:
                    self.smear = self.smear_1
                else:
                    self.smear = self.smear_2

            self.smear_pos = self.pos
            self.smear_angle = self.angle
    
    def get_pos(self):
        rad_angle = math.radians(self.angle_relative_to_body)
        self.pos = (WIDTH/2-math.cos(rad_angle)*self.distance_from_body, 
                    HEIGHT/2-math.sin(rad_angle)*self.distance_from_body)
        
    def get_side(self, factor=0):
        if self.angle_relative_to_body > 90 and self.angle_relative_to_body < 270:
            self.side = 'right'
            self.angle = 225-self.angle_relative_to_body - factor
        else:
            self.side = 'left'
            self.angle = 45-self.angle_relative_to_body + factor

    def draw(self):
        if self.state == 'swing':
            blitRotate2(self, self.smear, self.smear_pos, self.smear_angle) 
        blitRotate(self)

    def state_handler(self, pos):
        if self.state == 'idle':
            self.angle_relative_to_body, _ = trig(pos, screen_center, degrees=True, bound=True)
            self.get_pos()
            self.get_side()
            

        elif self.state == 'swing':            
            self.angle_relative_to_body = self.swing_angle
            self.get_pos()
            self.get_side(factor=self.swing_angle_corrective_factor)

    def update(self, pos):
        self.handle_cooldown()
        self.state_handler(pos)
        self.draw()
        


def draw_player():
    pygame.draw.circle(screen, (0, 0, 255), (WIDTH/2, HEIGHT/2), 10)

def blitRotate(sprite):
    a, b, w, h = sprite.image.get_rect()
    
    sin_a, cos_a = math.sin(math.radians(sprite.angle)), math.cos(math.radians(sprite.angle)) 
    min_x, min_y = min([0, sin_a*h, cos_a*w, sin_a*h + cos_a*w]), max([0, sin_a*w, -cos_a*h, sin_a*w - cos_a*h])

    pivot = pygame.math.Vector2(sprite.center_x, -sprite.center_y)# calculate the translation of the pivot 
    pivot_rotate = pivot.rotate(sprite.angle)
    pivot_move   = pivot_rotate - pivot

    origin = (sprite.pos[0] - sprite.center_x + min_x - pivot_move[0],
              sprite.pos[1] - sprite.center_y - min_y + pivot_move[1])#calculate the upper left origin of the rotated image
    
    rotated_image = pygame.transform.rotozoom(sprite.image, sprite.angle, 1)

    sprite.rect = rotated_image.get_rect()
    
    sprite.rect.x += sprite.pos[0] - sprite.center_x + min_x - pivot_move[0] 
    sprite.rect.y += sprite.pos[1] - sprite.center_y - min_y + pivot_move[1] 

    screen.blit(rotated_image, origin)

def blitRotate2(sprite, image, pos, angle):
    a, b, w, h = image.get_rect()
    x, y = pos

    center_x, center_y = w/2, h/2
    
    sin_a, cos_a = math.sin(math.radians(angle)), math.cos(math.radians(angle)) 
    min_x, min_y = min([0, sin_a*h, cos_a*w, sin_a*h + cos_a*w]), max([0, sin_a*w, -cos_a*h, sin_a*w - cos_a*h])

    pivot = pygame.math.Vector2(center_x, -center_y)# calculate the translation of the pivot 
    pivot_rotate = pivot.rotate(angle)
    pivot_move   = pivot_rotate - pivot

    origin = (x - center_x + min_x - pivot_move[0],
              y - center_y - min_y + pivot_move[1])#calculate the upper left origin of the rotated image
    
    rotated_image = pygame.transform.rotozoom(image, angle, 1)

    screen.blit(rotated_image, origin)

sword = Sword()

def trig(c1, c2, degrees=False, bound=True):
    dx = c2[0]-c1[0]
    dy = c2[1]-c1[1]
    angle = math.atan2(dy, dx)
    distance = math.hypot(dx, dy)

    if degrees:
        angle = bound_angle(math.degrees(angle))

    return angle, distance

while True:
    screen.fill((0,0,0))
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
    state = pygame.mouse.get_pressed()
    if state[0]:
        sword.swing()

    draw_player()

    pos = pygame.mouse.get_pos()
    sword.update(pos)

    pygame.display.update()