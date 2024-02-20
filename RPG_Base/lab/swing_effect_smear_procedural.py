import pygame, sys
import math

pygame.init()
WIDTH, HEIGHT = 400,400
screen_center = (WIDTH/2, HEIGHT/2)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def bound_angle(angle):
    if angle < 0:
        return 360+angle
    return angle

class Sword(pygame.sprite.Sprite):
    def __init__(self):
        self.angle = 0
        self.swing_angle = 0
        self.distance_from_body = 100
        self.normal_distance_from_body = 100
        self.swing_distance_from_body = 100

        self.hilt_dist = 30
        self.hilt_pos = (0,0)
        self.tip_dist = 120
        self.tip_pos = (0,0)


        img = pygame.image.load("data/sword_2.png").convert_alpha()
        img.set_colorkey((255,255,255))
        self.image = pygame.transform.scale(img, [x*4 for x in img.get_size()]).convert_alpha()

        self.smear_pos = (0,0)
        self.smear_angle = self.angle


        self.rect = self.image.get_rect()
        self.width, self.height = self.rect[2], self.rect[3]
        self.center_x, self.center_y = self.rect[2]/2, self.rect[3]/2

        self.state = 'idle'
        self.side = 'left'
        self.swing_cooldown = 0
        self.MAX_SWING_COOLDOWN = 100
        self.angle_relative_to_body = 0

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

            print(f"Angle Rel 2 Body: {self.angle_relative_to_body}")

            da = 90
            if self.side == 'right':
                self.swing_angle = self.angle_relative_to_body + da

            else:
                self.swing_angle = self.angle_relative_to_body - da

            self.smear_pos = self.pos
            self.smear_angle = self.angle

    def calculate_components(self):
        rad_angle = math.radians(self.angle_relative_to_body)

        da = 1
        if self.side == 'left':
            da = -1

        self.tip_pos = (self.pos[0] - da*math.sin(rad_angle)*self.tip_dist, 
                        self.pos[1] + da*math.cos(rad_angle)*self.tip_dist)
        self.hilt_pos = (self.pos[0] - da*math.sin(rad_angle)*self.hilt_dist, 
                        self.pos[1] + da*math.cos(rad_angle)*self.hilt_dist)
        
        pygame.draw.circle(screen, (255, 0, 0), self.tip_pos, 30)
        pygame.draw.circle(screen, (255, 255, 0), self.hilt_pos, 30)


      
    def update(self, pos):
        self.handle_cooldown()
        if self.state == 'idle':
            self.angle_relative_to_body, _ = trig(pos, screen_center, degrees=True, bound=True)
            print(f"Angle Rel: {bound_angle(self.angle_relative_to_body)}")
            rad_angle = math.radians(self.angle_relative_to_body)
            self.pos = (WIDTH/2-math.cos(rad_angle)*self.distance_from_body, 
                        HEIGHT/2-math.sin(rad_angle)*self.distance_from_body)
            


            if self.angle_relative_to_body > 90 and self.angle_relative_to_body < 270:
                self.side = 'right'
                self.angle = 225-self.angle_relative_to_body
                
            else:
                self.side = 'left'
                self.angle = 45-self.angle_relative_to_body

            self.calculate_components()

            


        elif self.state == 'swing':            
            self.angle_relative_to_body = self.swing_angle
            rad_angle = math.radians(self.angle_relative_to_body)
            self.pos = (WIDTH/2-math.cos(rad_angle)*self.distance_from_body, 
                        HEIGHT/2-math.sin(rad_angle)*self.distance_from_body)
            
            

            if self.angle_relative_to_body > 90 and self.angle_relative_to_body < 270:
                self.side = 'right'
                self.angle = 225-self.angle_relative_to_body

            else:
                self.side = 'left'
                self.angle = 45-self.angle_relative_to_body


        pygame.draw.circle(screen, (255, 0, 0), self.pos, 10)

            
        blitRotate(self)

      


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

    #sprite.rect = rotated_image.get_rect()
    
    #sprite.rect.x += x - center_x + min_x - pivot_move[0] 
    #sprite.rect.y += y - center_y - min_y + pivot_move[1] 

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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                sword.swing()

    draw_player()

    pos = pygame.mouse.get_pos()
    sword.update(pos)

    pygame.display.update()