import pygame, sys, os

pygame.init()
WIDTH, HEIGHT = 800,600
screen = pygame.display.set_mode((WIDTH, HEIGHT))#, flags=pygame.FULLSCREEN)
clock = pygame.time.Clock()

# TODO:
# 1) I implemented a rough version of cliffs, and now they somewhat work. However, the system is not robust
# --> ADDENDUM: The system is now pretty robust, but now there are errors with the cliff tileset, gaps and whatnot. Need to fix this and 
# ---> add in shadows or some kind of spacing
# 2) I need to add shadows to cliffs - seperate from art and to be done later
# 3) Clean up tileset

# NOTE:
# For the final implementation, find a way to more cleanly implement the cliffs (not necessarily a seperate tileset, but an extension of
# the original, max height of 3 perhaps?)


# Image prep functionality
from PIL import Image

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
    SECTION_END = (255,174,201)
    SECTION_START = (63,72,204)

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

# Get images
images = get_images("data/tileset_0.png")
cliffs = get_images("data/tileset_1.png")

images = [prep_image(img, 4) for img in images]
cliffs = [prep_image(img, 4) for img in cliffs]


# Begin Autotile elements
SIZE = 64

my_json = {4:0,5:1,1:2,0:3,6:4,7:5,3:6,2:7,
           14:8,15:9,11:10,10:11,12:12,13:13,9:14,8:15,
            31:16,135:17,39:18,79:19,142:20,239:21,191:22,43:23,78:24,
            223:25,127:26,27:27,47:28,77:29,29:30,143:31,134:32,
            167:33,175:34,35:35,207:36,111:37,255:38,59:39,206:40,999:41,159:42,63:43,
            76:44,95:45,93:46,25:47,256:48}

my_offsets = {10:-2, 11:-2, 14:-2, 15:-2, 23:-2, 27:-2, 39:-2, 47:-2}

def draw_grid():
    vert = WIDTH//SIZE + 5
    horz = HEIGHT//SIZE + 5

    for i in range(vert):
        pygame.draw.line(screen, (0,0,0), (i*SIZE, 0), (i*SIZE, HEIGHT*2))

    for i in range(horz):
        pygame.draw.line(screen, (0,0,0), (0, i*SIZE), (WIDTH*2, i*SIZE))


bitmap = [[0 for y in range(HEIGHT//SIZE + 1)] for x in range(WIDTH//SIZE + 1)]
summap = [[0 for y in range(HEIGHT//SIZE + 1)] for x in range(WIDTH//SIZE + 1)]
cliffsummap = [[0 for y in range(HEIGHT//SIZE + 1)] for x in range(WIDTH//SIZE + 1)]
imgmap = [[None for y in range(HEIGHT//SIZE + 1)] for x in range(WIDTH//SIZE + 1)]

direction_powers = {
    "up": 1,
    "right": 2,
    "down": 4,
    "left": 8,
    "up-left": 16,
    "up-right": 32,
    "down-left": 64,
    "down-right": 128,
}

def draw_bitmap(bitmap):
    for x, col in enumerate(bitmap):
        for y, val in enumerate(col):
            if val:
                pygame.draw.rect(screen, (255,0,0), (x*SIZE, y*SIZE, SIZE, SIZE))

def draw_tiles():
    num_rows = len(imgmap[0])
    num_cols = len(imgmap)

    for y in range(num_rows):
        for x in range(num_cols):
            img = imgmap[x][y]

            if img != None:
                x_offset = 0
                y_offset = 0
                val = my_json[cliffsummap[x][y]]

                if val in my_offsets:
                    x_offset = my_offsets[val]

                    screen.blit(img, (x*SIZE+x_offset*4, y*SIZE))

    for y in range(num_rows):
        for x in range(num_cols):
            img = imgmap[x][y]

            if img != None:
                val = my_json[cliffsummap[x][y]]

                if val not in my_offsets:
                    screen.blit(img, (x*SIZE, y*SIZE))

def get_pos(pos):
    x = pos[0]//SIZE
    y = pos[1]//SIZE

    return x, y

def find_neighbors(x, y):
    """Finds the neighbors with a value of 1 in a 2D grid, returning their relative directions.

   Args:
       x: The x-coordinate of the input cell.
       y: The y-coordinate of the input cell.

   Returns:
       A list of tuples, where each tuple contains (direction, neighbor_x, neighbor_y).
   """
    cardinal_directions = {'up': (0, -1, 1), 
                           'right': (1, 0, 2), 
                           'down': (0, 1, 4), 
                           'left': (-1, 0, 8)}
    
    diagonal_directions = {'up-left': (-1, -1, 16), 
                           'up-right': (1, -1, 32), 
                           'down-left': (-1, 1, 64), 
                           'down-right': (1, 1, 128)}
   
    neighbors = {}
    total = 0

    for direction, item in cardinal_directions.items():
        dx, dy, val = item
        neighbor_x = x + dx
        neighbor_y = y + dy

        if (0 <= neighbor_x < len(bitmap) and 0 <= neighbor_y < len(bitmap[0])):
            if bitmap[neighbor_x][neighbor_y]:
                neighbors[direction] = (neighbor_x, neighbor_y)
                total += val
            else:
                garbage = []
                for key, _ in diagonal_directions.items():
                    if direction in key:
                        garbage.append(key)
                for g in garbage:
                    del diagonal_directions[g]

    for key, item in diagonal_directions.items():
        dx, dy, val = item
        neighbor_x = x + dx
        neighbor_y = y + dy

        if (0 <= neighbor_x < len(bitmap) and 0 <= neighbor_y < len(bitmap[0])):
            if bitmap[neighbor_x][neighbor_y]:
                neighbors[key] = (neighbor_x, neighbor_y)
                total += val

    return neighbors, total

def update_summap(x,y):
    neighbors, val = find_neighbors(x, y)
    summap[x][y] = val
    print(my_json[val])
    imgmap[x][y] = images[my_json[val]]

    for _, item in neighbors.items():
        x, y = item
        _, val = find_neighbors(x, y)
        summap[x][y] = val
        imgmap[x][y] = images[my_json[val]]

def update_summap_cliffs(x,y):
    neighbors, val = find_neighbors(x, y)
    cliffsummap[x][y] = val
    imgmap[x][y] = cliffs[my_json[val]]

    for _, item in neighbors.items():
        x, y = item
        _, val = find_neighbors(x, y)
        cliffsummap[x][y] = val
        imgmap[x][y] = cliffs[my_json[val]]

def autotile():
    pass


while True:
    screen.fill((255, 255, 255))
    clock.tick(60)

    pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = get_pos(pos)
                
                bitmap[x][y] = int(not bitmap[x][y])
                update_summap(x, y)

                if not bitmap[x][y]:
                    imgmap[x][y] = None

            elif event.button == 3:
                x, y = get_pos(pos)
                
                bitmap[x][y] = int(not bitmap[x][y])*2
                update_summap_cliffs(x, y)

                if not bitmap[x][y]:
                    imgmap[x][y] = None
        
        
    draw_grid()
    draw_tiles()

    pygame.display.flip()

