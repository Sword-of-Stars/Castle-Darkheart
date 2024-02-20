import pygame, sys
import math

pygame.init()
WIDTH, HEIGHT = 400,400
screen = pygame.display.set_mode((WIDTH, HEIGHT))



class Sword(pygame.sprite.Sprite):
    def __init__(self):
        img = pygame.image.load("data/sword_2.png").convert_alpha()
        img.set_colorkey((255,255,255))
        self.image = pygame.transform.scale(img, [x*4 for x in img.get_size()]).convert_alpha()

        self.angle = 0
        self.swing_angle = 0
        self.distance_from_body = 100

        self.rect = self.image.get_rect()
        self.width, self.height = self.rect[2], self.rect[3]
        self.center_x, self.center_y = self.rect[2]/2, self.rect[3]/2

    def update(self, pos):
        c2 =(WIDTH/2, HEIGHT/2)
        angle, distance = trig(pos, c2)
        self.pos = (WIDTH/2-math.cos(angle)*self.distance_from_body, 
                    HEIGHT/2-math.sin(angle)*self.distance_from_body)
        pygame.draw.circle(screen, (255, 0, 0), self.pos, 10)


        if abs(math.degrees(angle)) > 90:
            self.angle = -135+math.degrees(270-angle) + self.swing_angle
            change = 1
        else:
            self.angle = 45-math.degrees(angle) + self.swing_angle
            change = -1

        state = pygame.mouse.get_pressed()
        if state[0]:
            self.swing_angle -= change
        else:
            self.swing_angle = 0
        
            
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

def blitRotate2(sprite):
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

sword = Sword()

def trig(c1, c2):
    dx = c2[0]-c1[0]
    dy = c2[1]-c1[1]
    angle = math.atan2(dy, dx)
    distance = math.hypot(dx, dy)
    return angle, distance

while True:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    draw_player()

    pos = pygame.mouse.get_pos()
    sword.update(pos)

    pygame.display.update()