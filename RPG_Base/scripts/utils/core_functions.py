from PIL import Image
import pygame, math, json

def collision_list(obj, obj_list):
    hit_list = []
    for r in obj_list:
        if obj.colliderect(r.rect):
            hit_list.append(r)
    return hit_list

def circle_collide(c1_pos, c1_rad, c2_pos, c2_rad):
    dist = distance(c1_pos, c2_pos)

    if dist < (c1_rad+c2_rad):
        return True
    
    return False

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

def angle_to(e1, e2):
    """Returns the angle from e1 to e2

    Arg:
        e1, e2 (seq): x-y coordinates
    Returns:
        float: angle in degrees
    """

    dx = e2[0]-e1[0]
    dy = e2[1]-e1[1]
    angle = math.degrees(math.atan2(dy,dx))
   
    return angle

def angle_to_rad(e1, e2):
    """Returns the angle from e1 to e2

    Arg:
        e1, e2 (seq): x-y coordinates
    Returns:
        float: angle in radians
    """

    dx = e2[0]-e1[0]
    dy = e2[1]-e1[1]
    angle = math.atan2(dy,dx)
   
    return angle

def distance(e1, e2):
    dx = e2[0]-e1[0]
    dy = e2[1]-e1[1]
    return math.hypot(dx, dy)

def blitRotateCenter(surf, image, topleft, angle):
    """Rotates an image about its center. 

    This is a faster method for its specific use case. For rotating about an 
    arbitrary pivot point, use the more generic function 'blitRotate'
    """

    rotated_image = pygame.transform.rotozoom(image, angle, 1)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = topleft).center)

    surf.blit(rotated_image.convert_alpha(), new_rect)

def blitRotate(surf, image, pos, originPos, angle):
    """Rotates an image about an arbitrary pivot point. 
    
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

def load_json(path):
    with open(f"{path}.json", "r") as load_file:
        file = json.load(load_file)
    return file

def world_to_screen(world_coords, offset, scale=1):
    world_x, world_y = world_coords
    offset_x, offset_y = offset
    screen_x = (world_x - offset_x)*scale
    screen_y = (world_y - offset_y)*scale
    return [screen_x, screen_y]