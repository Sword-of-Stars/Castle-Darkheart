import pygame
import json
import os
import importlib

CHUNK_DIVISOR = 4
SIZE = 64

#-- Screen/World Transforms --#

def world_to_screen(world_coords, offset, scale=1):
    world_x, world_y = world_coords
    offset_x, offset_y = offset
    screen_x = (world_x - offset_x)*scale
    screen_y = (world_y - offset_y)*scale
    return [screen_x, screen_y]

def screen_to_world(screen_coords, offset, scale=1):
    screen_x, screen_y = screen_coords
    offset_x, offset_y = offset
    world_x = (screen_x/scale) + offset_x
    world_y = (screen_y/scale) + offset_y
    return [world_x, world_y]

'''def world_to_screen(world_coords, offset, SIZE=SIZE, scale=1):
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
    return [int(world_x//SIZE), int(world_y//SIZE)]'''

def screen_to_chunk(pos, offset):
    return get_chunk_id(screen_to_world(pos, offset))

def get_chunk_id(pos):
    x, y = pos
    #divisor = CHUNK_SIZE/SIZE
    divisor = CHUNK_DIVISOR
    return f"{x//divisor};{y//divisor}"

def screen_to_chunk2(pos, offset):
    return get_chunk_id2(screen_to_world(pos, offset))

def get_mouse_info():
    rel = pygame.mouse.get_rel()
    state = pygame.mouse.get_pressed()
    pos = pygame.mouse.get_pos()
    return rel, state, pos

def render_text(font, msg, pos, screen, color=(255,255,255)):
    screen.blit(font.render(msg, False, color), pos)

#-- File Loading and Prep --#

def load_json(path):
    with open(f"{path}.json", "r") as load_file:
        file = json.load(load_file)
    return file

def get_asset_files(directory, extension=".png"):
    """
    Takes a directory and returns the names of all files within

    Returns a list of strings
    """
    files = []
    for entry in os.scandir(directory):
        if entry.is_file() and entry.name.endswith(extension):
            x = os.path.basename(entry.path)
            x = str(x).replace(extension, "")
            files.append(x)
    return files

def prep_image(img, scale, colorkey=(255,255,255)):
      rect = img.get_rect()
      img = pygame.transform.scale_by(img, scale)
      img.set_colorkey(colorkey)
      return img

def prep_image2(path, scale, colorkey=(255,255,255)):
    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.scale_by(img, scale)
    img.set_colorkey(colorkey)

    return img

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

#-- Dynamic Function Handling --#

def set_function(function):
    if function != "":
        module = importlib.import_module("config.functions") 
        if hasattr(module, function):
            return getattr(module, function)
        else:
            print(f"Function {function} not found")
    return None


