import pygame, sys, os
import random
import math
from memory_profiler import profile

# This is a test to determine whether my chunk system is good to use. Using
# databases and hashmaps, this gets a good average of how things work

# Perhaps minimizing screen_to_world calls 16x by using OOP for chunks?
# Regardless, this runs at ~300 fps average, with minimum of ~130 fps

# Next steps, good enough. Isolate and librarize, then incorporate into chunk loader!

WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.init()
clock = pygame.time.Clock()

os.chdir(f"{os.getcwd()}\\lab\\chunk_system")

# Variables
SIZE = 64
CHUNK_SIZE = 256
CHUNK_DIVISOR = 4

tile_0 = pygame.transform.scale_by(pygame.image.load("block.png").convert_alpha(), CHUNK_DIVISOR)
tile_1 = pygame.transform.scale_by(pygame.image.load("block_2.png").convert_alpha(), CHUNK_DIVISOR)
tile_2 = pygame.transform.scale_by(pygame.image.load("block3.png").convert_alpha(), CHUNK_DIVISOR)


database = {0:tile_0, 1:tile_1, 2:tile_2}
world_map = {}

# Functions

def world_to_screen(world_coords, offset, SIZE=SIZE, scale=1):
    world_x, world_y = world_coords
    offset_x, offset_y = offset
    screen_x = (world_x*SIZE - offset_x)*scale
    screen_y = (world_y*SIZE - offset_y)*scale
    return [screen_x, screen_y]

def screen_to_world(screen_coords, offset, SIZE=SIZE, scale=1):
    screen_x, screen_y = screen_coords
    offset_x, offset_y = offset
    world_x = (screen_x/scale) + offset_x
    world_y = (screen_y/scale) + offset_y
    return [int(world_x//SIZE), int(world_y//SIZE)]

def screen_to_chunk(pos, offset):
    return get_chunk_id(screen_to_world(pos, offset))

def get_chunk_id(pos):
    x, y = pos
    #divisor = CHUNK_SIZE/SIZE
    divisor = CHUNK_DIVISOR
    return f"{x//divisor};{y//divisor}"

def screen_to_chunk2(pos, offset):
    return get_chunk_id2(screen_to_world(pos, offset))

def get_chunk_id2(pos):
    x, y = pos
    #divisor = CHUNK_SIZE/SIZE
    divisor = CHUNK_DIVISOR
    return (x//divisor, y//divisor)

def generate_world():
    world_map = {}
    for x in range(-1000, 1000):
        for y in range(-10, 10):
            new_chunk(world_map, x, y)
    
    return world_map

def new_chunk(world_map, x, y):
    world_map[f"{x};{y}"] = [{"tile_ID":random.randint(0,2), "pos":[a,b]} for a in range(4) for b in range(4)]


def new_chunk_slow(world_map, x, y):
    world_map[f"{x};{y}"] = [{"tile_ID":random.choice([tile_0, tile_1, tile_2]), "pos":[a,b]} for a in range(4) for b in range(4)]

def draw_chunk(chunk, pos):
    x, y = [int(x) for x in pos.split(";")]
    for i in chunk:
        img = database[i['tile_ID']]
        px, py = i['pos']
        screen.blit(img, (world_to_screen((x*CHUNK_DIVISOR+px, y*CHUNK_DIVISOR+py), camera.offset)))

def draw_chunk_slow(chunk, pos):
    x, y = [int(x) for x in pos.split(";")]
    for i in chunk:
        img = i['tile_ID']
        px, py = i['pos']
        screen.blit(img, (world_to_screen((x*CHUNK_DIVISOR+px, y*CHUNK_DIVISOR+py), camera.offset)))

def draw_world(world_map):
    visible = camera.get_visible_chunks()
    for i in visible:
        draw_chunk(world_map[i], i)


# Objects

class Camera():
    def __init__(self, WIDTH, HEIGHT):
        self.rect = pygame.Rect(0,0,WIDTH,HEIGHT)
        self.offset = [-80,-5]

    def get_visible_chunks(self):
        tlx, tly = screen_to_world(self.rect.topleft, self.offset)
        brx, bry = screen_to_world(self.rect.bottomright, self.offset)

        '''for x in range(tlx, brx+1):
            for y in range(tly, bry+1):
                pygame.draw.rect(screen, (255, 0, 0), (*world_to_screen((x,y), self.offset), SIZE, SIZE), 4)'''

        ax, ay = screen_to_chunk2(self.rect.topleft, self.offset)
        bx, by = screen_to_chunk2(self.rect.bottomright, self.offset)

        c_dx = bx-ax+1
        c_dy = by-ay+1
        
        chunk_map = []
    
        for x in range(c_dx):
            for y in range(c_dy):
                chunk_map.append(f"{ax+x};{ay+y}")
                pygame.draw.rect(screen, (127, 0, 255), (*world_to_screen(((ax+x)*CHUNK_DIVISOR,(ay+y)*CHUNK_DIVISOR), 
                                                                          self.offset), CHUNK_SIZE, CHUNK_SIZE), 1)
                    
        #pygame.draw.circle(screen, (255, 255, 0, 100), world_to_screen((ax*CHUNK_DIVISOR+4, ay*CHUNK_DIVISOR+4), self.offset), 10)
        #pygame.draw.circle(screen, (100, 255, 32), world_to_screen((bx*CHUNK_DIVISOR-4, by*CHUNK_DIVISOR-4), self.offset), 5)

        return chunk_map


    def update(self):
        pass

class World():
    def __init__(self):
        pass

# Instantiation
camera = Camera(WIDTH, HEIGHT)
camera.get_visible_chunks()

direction = -1

world = generate_world()

lowest_fps = 1000
tot_fps = 0
frame = 0

while True:
    clock.tick(0)
    screen.fill((0,0,0))
    
    frame += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pos = pygame.mouse.get_pos()
    #pygame.display.set_caption(str(screen_to_chunk(pos, camera.offset)))
    x = clock.get_fps()
    tot_fps += x
    if x < lowest_fps and x!= 0:
        lowest_fps = x
    pygame.display.set_caption(f"{lowest_fps},  {round(tot_fps/frame, 5)}")

    camera.offset[0] += math.sin(frame/1000)*10
    #camera.offset[1] += direction

    camera.get_visible_chunks()

    draw_world(world)

    pygame.display.flip()
    
