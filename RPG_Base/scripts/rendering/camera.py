import pygame
import random

from scripts.rendering.shaders import ShaderContext

# To avoid passing 'camera' and 'screen' to every f*cking function, I'll just pass a single camera
# object instead
# All sprites will be drawn on the camera surface, and the camera display will be scaled up to the 
# screen dimensions

SIZE = 64
CHUNK_DIVISOR = 4

def screen_to_chunk(pos, offset):
    return get_chunk_id(screen_to_world(pos, offset))

def screen_to_tile(pos, offset):
    return get_tile_pos(screen_to_world(pos, offset))

def get_chunk_id(pos):
    x, y = pos
    #divisor = CHUNK_SIZE/SIZE
    divisor = CHUNK_DIVISOR
    return (x//divisor, y//divisor)

def get_tile_pos(pos):
    x, y = pos
    #divisor = CHUNK_SIZE/SIZE
    divisor = CHUNK_DIVISOR
    return (x%4, y%4)


def screen_to_world(screen_coords, offset, SIZE=SIZE, scale=1):
    screen_x, screen_y = screen_coords
    offset_x, offset_y = offset
    world_x = (screen_x/scale) + offset_x
    world_y = (screen_y/scale) + offset_y
    return [int(world_x//SIZE), int(world_y//SIZE)]

def get_visible_chunks(self):
       
        ax, ay = screen_to_chunk(self.rect.topleft, self.offset)
        bx, by = screen_to_chunk(self.rect.bottomright, self.offset)

        c_dx = bx-ax
        c_dy = by-ay
        
        chunk_map = []
    
        for x in range(c_dx): # add a buffer for seamless loading
            for y in range(c_dy):
                chunk_map.append(f"{ax+x};{ay+y}")

        return chunk_map

class Camera():
    # TODO: Move all camera values (x,y) into a rect
    # TODO: Make camera scale by 4x
    # TODO: Integrate shaders
    def __init__(self, x, y, width, height, scale=1.0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.scale = scale

        self.speed = 0.05

        self.render_list = []

        self.display = pygame.Surface((width, height))
        self.new_display = pygame.Surface((width, height))

        self.rect = self.display.get_rect(x=x, y=y)

        self.ui_surf = pygame.Surface((width, height), pygame.SRCALPHA)

        self.ctx = ShaderContext()


        self.screen_shake = False
        self.screen_shake_x = []
        self.screen_shake_y = []

        self.vignette = 0.6
        self.vignette_1 = 0.2

    def reset(self):
        self.x = 0
        self.y = 0

    def fill(self):
        self.render_list = []
        self.display.fill((0,0,0))

    def set_screen_shake(self, val, magnitude=[3,1]):
        self.screen_shake = True
        self.screen_shake_x = [random.randint(-magnitude[0], magnitude[0]) for x in range(val//2)]
        self.screen_shake_x + self.screen_shake_x[::-1]

        self.screen_shake_y = [random.randint(-magnitude[1], magnitude[1]) for x in range(val//2)]
        self.screen_shake_y + self.screen_shake_y[::-1]


    def move(self, player):
        dx = player.rect.x - self.width/2
        dy = player.rect.y - self.height/2

        # calculate new camera position using smoothing function
        self.x += int(dx * self.speed)
        self.y += int(dy * self.speed)

        return dx, dy
    
    def pos_to_tile(self, pos):
        return screen_to_chunk(pos, (self.x, self.y)), screen_to_tile(pos, (self.x, self.y))

    def get_visible_chunks(self):
       
        ax, ay = screen_to_chunk(self.rect.topleft, (self.x, self.y))
        bx, by = screen_to_chunk(self.rect.bottomright, (self.x, self.y))

        c_dx = bx-ax+1 # +1 adds a bit of buffer for seamless drawing
        c_dy = by-ay+1
        
        chunk_map = []
    
        for x in range(-1, c_dx):
            for y in range(-1, c_dy):
                chunk_map.append(f"{ax+x};{ay+y}")
                    
        return chunk_map
    
    def to_render(self, object):
        '''Push items to be rendered to the screen. The camera handles z-ordering and shader effects.'''

        # Remove checking after
        assert type(object.layer) is not None

        self.render_list.append(object)

    def draw_world(self):
        '''Draws everything in the render list to the screen using z-ordering'''
        # sort the world by y order as well

        # Only draw tiles that are supposed to be on screen, eventually implement y ordering
       
        for item in sorted(self.render_list, key=lambda x: (x.layer, x.rect.y, x.rect.x)): # , x.rect.y)):
            item.draw(self)

    def update(self):
        pos = (0,0)
        if self.screen_shake_x != [] and self.screen_shake_x != []:
            pos = (self.screen_shake_x.pop(), self.screen_shake_y.pop())
        
        self.new_display.blit(self.display, pos)

        self.ctx.update(self.new_display, self.ui_surf, self.vignette, self.vignette_1)

