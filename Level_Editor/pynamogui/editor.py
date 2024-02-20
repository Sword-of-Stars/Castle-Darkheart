import pygame, sys, os
import math

from misc import core_functions as cf
from gui_elements.regions import Region

from PIL import Image

# WORKFLOW
# --------
# 1) Click on folder name
# 2) Generate and split tilesets, save to reduce redundancy
#    - Perhaps make a dataset structure
# 3) Place tiles and save files

pygame.init()
WIDTH, HEIGHT = 1200,750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Level Editor v1.0")
clock = pygame.time.Clock()

font = pygame.font.Font('data/at01.ttf', 50)
font_small = pygame.font.Font('data/at01.ttf', 30)

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

SIZE = 64

#-- Functions --#
def top_text(folder=None, mode=None, layer=None):
   """
   Draw the text on the top of the screen

   Parameters
   ----------
   folder : str
      The name of the folder the displayed assets are from
   mode : str
      The current mode (list options here)
   layer : int
      The active layer (fore (0), middle (1) and background (2))

   Local Variables
   ---------------
   color : tuple
      Color of the text
   folder_, mode_, layer_pos : tuple
      Position of each text along the top of the screen

   """
   color = (255, 255, 255)
   folder_pos = (330, 10)
   if folder != None:
      screen.blit(cf.draw_text(folder, color, font_small), folder_pos)
   
   mode_pos = (630, 10)
   if mode != None:
      screen.blit(cf.draw_text(f"Mode: {mode}", color, font_small), mode_pos)
   
   layer_pos = (1100, 10)
   if layer != None:
      screen.blit(cf.draw_text(f"Layer: {str(layer)}", color, font_small), layer_pos)

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

def get_images(spritesheet, dimensions, scale=True):
   if len(spritesheet.getpixel((0,0))) == 4: #If alpha channel included
      SECTION_START = (255,0,255,255)
      SECTION_END = (63,72,204,255)
      form = 'RGBA'
   else:
      SECTION_START = (255,0,255)
      SECTION_END = (63,72,204)
      form = 'RGB'

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
      img = pygame.image.fromstring(image_bytes, img.size, form)

      # Scale image to desired dimensions
      if scale:
         #img = scale_image(img, *dimensions)
         img = cf.scale_pixel_image(img)
      images.append(img)

   return images

def scale_image(img, width, height):
   imgw, imgh = img.get_size()
   scalex = width/imgw
   scaley = height/imgh
   
   invscalex = imgw/width
   invscaley = imgh/height

   if scalex < 1 or scaley < 1: #if the image size is larger than the designated width and height
      scale_factor = min(scalex, scaley)
      new_size = (scale_factor*imgw, scale_factor*imgh)
      return pygame.transform.scale(img, new_size).convert_alpha()
   
   elif invscalex < 1 or invscaley < 1: #if the image size is larger than the designated width and height
      scale_factor = max(invscalex, invscaley)
      new_size = (scale_factor*width, scale_factor*height)
      return pygame.transform.scale(img, new_size).convert_alpha()
   
   return img

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

def get_mouse_info():
    rel = pygame.mouse.get_rel()
    state = pygame.mouse.get_pressed()
    pos = pygame.mouse.get_pos()
    return rel, state, pos

class Editor():
   def __init__(self, images):
      self.regions = {"map":World((301,50,WIDTH-301,HEIGHT-50)),
                      "headers":Headers((0,0,300,201), None),
                      "palette":ScrollBox((0,200,300,451), images),
                      "load_save":Load_Save((0,650,300,HEIGHT-650)),
                      "box_top":BoxTop((299,0,WIDTH-299,50))}


   def handle_scroll(self, event, pos):
      if self.regions["palette"].rect.collidepoint(pos):
         self.regions["palette"].scroll_event(event, pos)
      elif self.regions["map"].rect.collidepoint(pos):
         self.regions["map"].scroll_event(event, pos)

   def update(self, pos, state):
      for key, region in self.regions.items():
         region.update(pos, state) 

class Builder():
   def __init__(self):
      self.selected = None
   def get_selected(self, palette):
      self.selected = palette.selected
   def update(self, pos):
      if self.selected != None:
         w, h = self.selected['rect'].width, self.selected['rect'].height
         x, y = pos
         screen.blit(self.selected['img'], (x-w/2, y-h/2))

if __name__ == "__main__":
   with Image.open("data/blue_decor.png") as img:
      images = get_images(img, (50, 50))

   editor = Editor(images)
   builder = Builder()

   while True:
      clock.tick(60)
      screen.fill((0,0,0))

      rel, state, pos = get_mouse_info()
      if state[0] and builder.selected == None:
         editor.regions['map'].pan(pos, rel)

      editor.update(pos, state)
      world_before_zoom = screen_to_world(pos, editor.regions["map"].offset, editor.regions["map"].scale)



      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
         elif event.type == pygame.MOUSEWHEEL:
            editor.handle_scroll(event, pos)

      world_after_zoom = screen_to_world(pos, editor.regions["map"].offset, editor.regions["map"].scale)
      editor.regions["map"].offset[0] += world_before_zoom[0] - world_after_zoom[0]
      editor.regions["map"].offset[1] += world_before_zoom[1] - world_after_zoom[1]


      builder.get_selected(editor.regions["palette"])
      builder.update(pos)

      pygame.display.update()

