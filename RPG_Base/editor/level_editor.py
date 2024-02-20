import pygame, sys, os
import math

import core_functions as cf

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

def draw_grid2(offset, topleft=(0,0), scale=1):
   num_lines_vertical = 11 # Number of lines extending from one side
   num_lines_horizontal = 13
   x, y = topleft
   x, y = 0,0
   world_origin = world_to_screen((offset), offset, scale)
   color = (255, 0, 0)

   for i in range(0, num_lines_horizontal+1): #Draw vertical lines
      top = world_to_screen((i*SIZE, 0), offset, scale)
      bottom = world_to_screen((i*SIZE, y+num_lines_vertical*SIZE), offset, scale)

      width = 1
      if i == 0:width = 5
      pygame.draw.line(screen, color, top, bottom, width=width)

   for i in range(0, num_lines_vertical+1): #Draw horizontal lines
      left = world_to_screen((x, y+i*SIZE), offset, scale)
      right = world_to_screen((x+num_lines_horizontal*SIZE, y+i*SIZE), offset, scale)

      width = 1
      if i == 0:width = 5
      pygame.draw.line(screen, color, left, right, width=width)

   #pygame.draw.circle(screen, (255,0,0), world_origin, 10)

def draw_grid3(offset, topleft=(0,0), scale=1, center=(0,0)):
   num_lines_vertical = 11 # Number of lines extending from one side
   num_lines_horizontal = 13
   x, y = topleft
   a,b = center
   world_origin = world_to_screen((0,0), (-a,-b), scale)
   color = (255, 0, 0)

   for i in range(0, num_lines_horizontal+1): #Draw vertical lines
      top = world_to_screen((x+i*SIZE, y), offset, scale)
      bottom = world_to_screen((x+i*SIZE, y+num_lines_vertical*SIZE), offset, scale)

      width = 1
      if i == 0:width = 5
      pygame.draw.line(screen, color, top, bottom, width=width)

   for i in range(0, num_lines_vertical+1): #Draw horizontal lines
      left = world_to_screen((x, y+i*SIZE), offset, scale)
      right = world_to_screen((x+num_lines_horizontal*SIZE, y+i*SIZE), offset, scale)

      width = 1
      if i == 0:width = 5
      pygame.draw.line(screen, color, left, right, width=width)

   pygame.draw.circle(screen, (255,0,0), world_origin, 10)

def draw_grid4(screen_coord_of_world_origin, offset, scale=1):
   pygame.draw.circle(screen, (255,0,0), screen_coord_of_world_origin, 10)
   num_horiz_lines = 5
   num_vert_lines = 4
   color=(255,0,0)
   offset = [-x for x in screen_coord_of_world_origin]
   #print(screen_to_world(screen_coord_of_world_origin, [-x for x in screen_coord_of_world_origin]))

   for i in range(-num_vert_lines, num_vert_lines+1): #Draw vertical lines
      top = world_to_screen((i*SIZE, -num_horiz_lines*SIZE), offset, scale)
      bottom = world_to_screen((i*SIZE, num_horiz_lines*SIZE), offset, scale)


      width = 1
      if i == 0:width = 5
      pygame.draw.line(screen, color, top, bottom, width=width)

   for i in range(-num_horiz_lines, num_horiz_lines+1): #Draw vertical lines
      left = world_to_screen((-num_vert_lines*SIZE, i*SIZE), offset, scale)
      right = world_to_screen((num_vert_lines*SIZE, i*SIZE), offset, scale)

      width = 1
      if i == 0:width = 5
      pygame.draw.line(screen, color, left, right, width=width)

def draw_grid5(screen_coord_of_world_origin, offset, rect, scale=1):
   pygame.draw.circle(screen, (255,0,0), screen_coord_of_world_origin, 10)
   num_vert_lines = rect.width//(SIZE*scale)//2
   num_horiz_lines = rect.height//(SIZE*scale)//2
   color=(255,0,0)

   for i in range(-num_vert_lines, num_vert_lines): #Draw vertical lines
      top = world_to_screen((i*SIZE, -(num_horiz_lines+1)*SIZE), offset, scale)
      bottom = world_to_screen((i*SIZE, (num_horiz_lines+1)*SIZE), offset, scale)

      width = 1
      if i == 0:width = 5
      pygame.draw.line(screen, color, top, bottom, width=width)

   for i in range(-num_horiz_lines, num_horiz_lines+1): #Draw horizontal lines
      left = world_to_screen((-num_vert_lines*SIZE, i*SIZE), offset, scale)
      right = world_to_screen((num_vert_lines*SIZE, i*SIZE), offset, scale)

      width = 1
      if i == 0:width = 5
      pygame.draw.line(screen, color, left, right, width=width)

def draw_grid6(screen_coord_of_world_origin, offset, rect, scale=1):
   pygame.draw.circle(screen, (255,0,0), screen_coord_of_world_origin, 10)
   num_vert_lines = int(rect.width//(SIZE*scale)//2)
   num_horiz_lines = int(rect.height//(SIZE*scale)//2)
   color=(255,0,0)

   for i in range(-num_vert_lines, num_vert_lines): #Draw vertical lines
      top = world_to_screen((i*SIZE, -(num_horiz_lines+1)*SIZE), offset, scale)
      bottom = world_to_screen((i*SIZE, (num_horiz_lines+1)*SIZE), offset, scale)

      width = 1
      if i == 0:width = 5
      pygame.draw.line(screen, color, top, bottom, width=width)

   for i in range(-num_horiz_lines, num_horiz_lines+1): #Draw horizontal lines
      left = world_to_screen((-num_vert_lines*SIZE, i*SIZE), offset, scale)
      right = world_to_screen((num_vert_lines*SIZE, i*SIZE), offset, scale)

      width = 1
      if i == 0:width = 5
      pygame.draw.line(screen, color, left, right, width=width)

def draw_grid7(screen_coord_of_world_origin, offset, rect, delta_offset, scale=1):
   # Effective, efficient, if crappy code
   pygame.draw.circle(screen, (255,0,0), screen_coord_of_world_origin, 10)
   num_vert_lines = rect.width//(SIZE*scale)
   dx = delta_offset[0]//(SIZE)
   left_limit = int(-num_vert_lines//2-dx-1)
   right_limit = int(num_vert_lines//2-dx+1)

   num_horiz_lines = rect.height//(SIZE*scale)
   dy = delta_offset[1]//(SIZE*scale)
   top_limit = int(-num_horiz_lines//2-dy-1)
   bottom_limit = int(num_horiz_lines//2-dy+1)

   color=(255,0,0)

   for i in range(left_limit, right_limit):
      x = screen_coord_of_world_origin[0]+(SIZE*scale*i)
      top = (x, rect.top)
      bottom = (x, rect.bottom)

      width = 1
      if i == 0:width = 5

      pygame.draw.line(screen, color, top, bottom, width=width)

   for i in range(top_limit, bottom_limit):
      y = screen_coord_of_world_origin[1]+(SIZE*scale*i)
      left = (rect.left, y)
      right = (rect.right, y)
      
      width = 1
      if i == 0:width = 5

      pygame.draw.line(screen, (255,0,0), left, right, width=width)
     
def draw_grid8(offset, scale, rect):
   num_lines = 20# Number of lines extending from one side
   num_vert_lines = int(rect.width//(SIZE*scale))

   world_origin = world_to_screen((0,0), offset, scale)
   color = (200, 100, 100)

   for i in range(-num_lines, num_lines+1): #Draw vertical lines
      top = world_to_screen((i*SIZE, -num_lines*SIZE), offset, scale)
      bottom = world_to_screen((i*SIZE, num_lines*SIZE), offset, scale)

      width = 1
      if i == 0:width = 5
      pygame.draw.line(screen, color, top, bottom, width=width)

   for i in range(-num_lines, num_lines+1): #Draw horizontal lines
      left = world_to_screen((-num_lines*SIZE, i*SIZE), offset, scale)
      right = world_to_screen((num_lines*SIZE, i*SIZE), offset, scale)

      width = 1
      if i == 0:width = 5
      pygame.draw.line(screen, color, left, right, width=width)

   pygame.draw.circle(screen, color, world_origin, 10)

def draw_grid8a(offset, scale, rect, size):
   l, r, u, d = size
   world_origin = world_to_screen((0,0), offset, scale)
   color = (200, 100, 100)

   for i in range(-l, r+1): #Draw vertical lines
      top = world_to_screen((i*SIZE, -u*SIZE), offset, scale)
      
      if top[0] < rect.left or top[0] > rect.right:
         # See if this optimization actually helps at all
         continue

      bottom = world_to_screen((i*SIZE, d*SIZE), offset, scale)

      top[1] = max(rect.top, top[1])
      bottom[1] = min(rect.bottom, bottom[1])

      width = 1
      if i == 0:width = 5
      pygame.draw.line(screen, color, top, bottom, width=width)

   for i in range(-u, d+1): #Draw horizontal lines
      left = world_to_screen((-l*SIZE, i*SIZE), offset, scale)

      if left[1] < rect.top or left[1] > rect.bottom:
         # See if this optimization actually helps at all
         continue

      right = world_to_screen((r*SIZE, i*SIZE), offset, scale)

      left[0] = max(rect.left, left[0])
      right[0] = min(rect.right, right[0])


      width = 1
      if i == 0:width = 5
      pygame.draw.line(screen, color, left, right, width=width)

   pygame.draw.circle(screen, color, world_origin, 10)

def draw_grid9(offset, scale, rect, delta_offset):
   num_lines = 20# Number of lines extending from one side

   num_vert_lines = int(rect.width//(SIZE*scale))
   #dx = int(delta_offset[0]//(SIZE*scale))
   #dx, dy = screen_to_world(delta_offset, offset, scale)
   print(num_vert_lines)
   dx = int(delta_offset[0]//(SIZE*scale))
   dy= int(delta_offset[1]//(SIZE*scale))
   print(f"dx: {dx}, dy: {dy}")
   num_horiz_lines = int(rect.height//(SIZE*scale))


   world_origin = world_to_screen((0,0), offset, scale)
   color = (200, 100, 100)

   num_vert_drawn = 0
   for i in range(-num_vert_lines//2-dx, num_vert_lines//2+1-dx): #Draw vertical lines
      top = world_to_screen((i*SIZE, -num_lines*SIZE), offset, scale)
      bottom = world_to_screen((i*SIZE, num_lines*SIZE), offset, scale)

      width = 1
      if i == 0:width = 5
      pygame.draw.line(screen, color, top, bottom, width=width)
      num_vert_drawn += 1

   print(f"Num Vert Drawn: {num_vert_drawn}")

   for i in range(-num_horiz_lines//2-dy, num_horiz_lines//2-dy+1): #Draw horizontal lines
      left = world_to_screen((-num_lines*SIZE, i*SIZE), offset, scale)
      right = world_to_screen((num_lines*SIZE, i*SIZE), offset, scale)

      width = 1
      if i == 0:width = 5
      pygame.draw.line(screen, color, left, right, width=width)

   pygame.draw.circle(screen, color, world_origin, 10)
#-- Classes --#
class Region():
   """
   Defines a colored region with a border on which elements are displayed

   Methods
   -------
   draw
      Draws the region and its border
   update
      displays the region on the screen 
      *designed to be overwritten by children
   """
   def __init__(self, x, y, width, height, body_color=(19, 46, 66), border_color=(113, 144, 227)):
      self.border_rect = pygame.rect.Rect(x, y, width, height)
      border_width = 1
      self.rect = pygame.rect.Rect(x+border_width, y+border_width, 
                                    width-2*border_width, height-2*border_width)
      
      self.body_color = body_color
      self.border_color = border_color

   def draw(self):
      pygame.draw.rect(screen, self.border_color, self.border_rect)
      pygame.draw.rect(screen, self.body_color, self.rect)

   def update(self, pos, state):
      self.draw()

class Headers(Region):
   """
   Generates a list of headers from relevant folders
   These headers can be hovered over and selected for navigation
   Inherits from Region

   Methods
   -------
   draw_text
      Displays the folder names and checks whether they're selected
   update
      Draws the region and its text

   """
   def __init__(self, rect, path):
      Region.__init__(self, *rect)
      self.path = path

      #-- Render folder names --#
      text_spacing = 30
      text_pos = (10,0)
      self.lst = get_asset_files(f"{dir_path}/data")
      self.names = {x:{
                  "pos":(text_pos[0],text_pos[1]+text_spacing*index),
                  "text":cf.draw_text(x, (255,255,255), font),
                  "rect":None}
                  for index, x in enumerate(self.lst)}
      for name in self.names:
         self.names[name]["rect"] = self.names[name]["text"].get_rect()
         self.names[name]["rect"].x, self.names[name]["rect"].y, = self.names[name]["pos"]

      self.selected_folder = None

   def draw_text(self, pos, state):
      is_over = False
      for key, name in self.names.items():
         x, y = name["pos"]
         if not is_over:
            if name["rect"].collidepoint(pos):
               is_over = True
               x += 10 # When hovering over text, extend to the right
               if state[0]:
                  self.selected_folder = key
         screen.blit(name["text"], (x,y))

   def update(self, pos, state):
      self.draw()
      self.draw_text(pos, state)
         
class Load_Save(Region):
   def __init__(self, rect):
      Region.__init__(self, *rect)

      icons = ["load", "save"]
      self.icons = {x: {"image": cf.prep_image(pygame.image.load(f"data/{x}.png"), 2), "rect": None} for x in icons}
      for x in self.icons:
         self.icons[x]["rect"] = self.icons[x]["image"].get_rect()

      # Generates icons of the style {"load":{"image":img, "rect", rect}}
      
      self.icons["load"]["rect"].x, self.icons["load"]["rect"].y = self.rect.x+160, self.rect.y+15
      self.icons["save"]["rect"].x, self.icons["save"]["rect"].y = self.rect.x+60, self.rect.y+15

      
   def draw_icons(self, pos, state):
      for key, icon in self.icons.items():
         x, y = icon["rect"].x, icon["rect"].y
         if icon["rect"].collidepoint(pos):
            y -= 5
            if state[0]:
               #os.startfile("data")
               print("load, save, whatever: need to make thing")
         screen.blit(icon["image"], (x, y))

   def update(self, pos, state):
      self.draw()
      self.draw_icons(pos, state)

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

class ScrollBox(Region):
      """
      Creates a box that can display a scrolling assortment of assets
      Inherits from Region

      Methods
      -------
      scroll_items
         Draws the desired images onto a subsurface in the proper position
      update
         Displays the scrolled assets
      """
      def __init__(self, rect, images, orientation="linear"):
         """
         Inheritance
         -----------
         Region
            A versatile class describing boxy regions for UI elements

         Parameters
         ----------
         rect : tuple
            Describes the x, y, width, height of the scrollbox
         orientation : str 
            (deprecated feature)
            Determines the layout of the assets in the scrollbox (linear or box)

         Attributes
         ----------
         subsurface : pygame.Surface
            Subsurface onto which scrolled images are drawn
         subsurface_colorkey : tuple
            Colorkey for the subsurface, currently set to obscure color
         scroll : int
            How far along the player has scrolled 
            0 is the default position, increases as user scrolls up
         scroll_max : int
            The maximum vertical distance the user can scroll
         images : dict
            A dictionary containing information on all images in scroll box
            Includes "img", "pos", and "rect"
         selected : unknown data type
            Whichever image is selected
         """
         # Create a child of Region
         Region.__init__(self, *rect)

         # Create the subsurface
         self.subsurface = pygame.Surface((rect[2]-2, rect[3]-2))
         self.subsurface_colorkey = (0,0,1)

         # Set positioning and spacing parameters
         offset = (20,-180)
         vertical_spacing = 10
         self.scroll = 0
         self.speed = 10
         self.selected = None

         # Load images and relevant information in dictionary
         self.images = {index:
                        {"img":img.convert_alpha()} 
                        for index, img in enumerate(images)}
         
         # Store the image rect values and positions in the self.images dict
         height = 0
         for index, name in enumerate(self.images):
            rect = self.images[name]["img"].get_rect()
            x = self.rect.x+offset[0]
            y = self.rect.y+height+offset[1]+vertical_spacing*(index-1)
            height += rect.height

            rect = self.images[name]["img"].get_rect(x=x, y=y)
            self.images[name]["pos"] = (x, y)
            self.images[name]["rect"] = rect
            self.images[name]["isover"] = False        
            self.images[name]["selected"] = False        

         # Calculate the max spacing by summing heights and vertical spacing
         # NOTE: There's a much better way to do this
         img_heights = 0
         for _, img in self.images.items():
            rect = img["img"].get_rect()
            img_heights += rect.height+vertical_spacing
         self.scroll_max = img_heights - self.rect.height + vertical_spacing


      def scroll_event(self, event, pos):
         if self.rect.collidepoint(pos):
            self.scroll -= event.y*self.speed

      def scroll_items(self):
         # Bind the scrolling values between 0 and self.scroll_max
         self.scroll = min(max(self.scroll, 0), self.scroll_max)
         
         # Prepares the subsurface for receiving the images
         self.subsurface.fill(self.subsurface_colorkey)
         self.subsurface.set_colorkey(self.subsurface_colorkey)
         self.subsurface.convert_alpha()

         # Blit the images to the subsurface
         for _, img in self.images.items():
            img["rect"].y = img["pos"][1]-self.scroll

            if img["isover"]:
                  x = img["pos"][0]+10
            else:
                  x = img["pos"][0]

            self.subsurface.blit(img["img"], (x, img["rect"].y))

      def select(self, pos, state):
         if self.rect.collidepoint(pos): # If the mouse is over the scroll box
            # Change mouse pos to accomodate for positional differences
            x, y = pos
            x -= self.rect.x
            y -= self.rect.y
            for _, img in self.images.items():
                  if img["rect"].collidepoint((x,y)):
                     img["isover"] = True
                     if state[0]:
                        self.selected = img
                  else:
                     img["isover"] = False

         if state[2]:
            self.selected = None

      def blit_subsurface(self):
         x, y = self.rect.topleft
         screen.blit(self.subsurface, (x+1, y+1))

      def update(self, pos, state):
         self.select(pos, state)
         self.draw() # Inherited from Region
         self.scroll_items()
         self.blit_subsurface()

class BoxTop(Region):
   def __init__(self, rect):
      Region.__init__(self, *rect)

   def update(self, state, pos):
      self.draw()
      top_text("Level Editor", "kill and destroy", 2)
     
class World(Region):
   def __init__(self, rect):
      Region.__init__(self, *rect, body_color=(0,0,0), border_color=(0,0,0))
      self.scale = 1 # Alter with scroll wheel
      self.offset = [-x for x in self.rect.center]
      self.original_offset = self.offset.copy()

      self.scale = 1
      self.scroll_speed = 0.1
      self.scroll_min = 0.25
      self.scroll_max = 4
      #self.size = {'left':0, 'right':0, 'up':0, "down":0}
      self.size = [0, 20, 15, 5]

   def draw_grid(self):
      center = world_to_screen((0,0), self.offset)
      delta_offset = (self.original_offset[0]+center[0], self.original_offset[1]+center[1])
      print(delta_offset)
      #draw_grid7(center, self.offset, self.rect, delta_offset, scale=self.scale)
      #draw_grid6(center, self.offset, self.rect,scale=self.scale)
      #draw_grid9(self.offset, self.scale,self.rect, delta_offset)
      draw_grid8a(self.offset, self.scale, self.rect, self.size)

   def pan(self, pos, rel):
      if self.rect.collidepoint(pos):
         self.offset[0] -= rel[0]/self.scale
         self.offset[1] -= rel[1]/self.scale

   def scroll_event(self, event, pos):
      self.scale = max(min(self.scale-event.y*self.scroll_speed, self.scroll_max), self.scroll_min)

   def update(self, pos, state):
      self.draw()
      self.draw_grid()

      x, y = screen_to_world(pos, self.offset, scale=self.scale)
      print(x//SIZE,y//SIZE)

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

