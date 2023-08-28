import pygame
import json
import importlib
import os
import functools

from PIL import Image

from ..misc.core_functions import get_asset_files, world_to_screen, screen_to_world, load_json, prep_image, get_images
from ..gui_elements.region import Region
from ..gui_elements.elements import Selectable, BuilderObject, SelectableCell
from ..builder.builder_functions import get_path_id, get_images_from_db

class BlankRegion(Region):
   def __init__(self, config):
      Region.__init__(self, *config['rect'])

class ImageBox(Region):
   def __init__(self, config, builder):
      Region.__init__(self, *config['rect'])
      self.builder = builder

      self.images = [{'img': prep_image(pygame.image.load(i['path']), i['scale']), 'is_active': False, **i} 
                     for i in config['images']]

      self.movable = config['movable']
      self.set_rects()
      self.set_functions()
      
   def set_rects(self):
      for img in self.images:
         rect = img['img'].get_rect()
         img['rect'] = pygame.Rect(self.rect.x+img['offset'][0], 
                                   self.rect.y+img['offset'][1],
                                   rect[2], rect[3])
         
   def set_functions(self):
      def rgetattr(obj, attr, *args):
         def _getattr(obj, attr):
            return getattr(obj, attr, *args)
         return functools.reduce(_getattr, [obj] + attr.split('.'))
      
      self.args = []
      module = importlib.import_module("config.functions") 
      for img in self.images:
         if hasattr(module, img['function']):
            function = getattr(module, img['function'])
            img['function'] = function

            # Only add arguments if the image has a function
            args = [rgetattr(self, arg) for arg in img['self_args']]
            for i in img['args']:
               args.append(i)
            img['args'] = args

         else:
            print(f"Function {img['function']} not found")
            img['function'] = None

   def draw_images(self, pos, state, screen):
      for image in self.images:
         x, y = image['rect'].topleft
         if image['rect'].collidepoint(pos):
            if self.movable:
               y -= 5
            if state[0] and not image['is_active']:
               image['is_active'] = True
               if image['function'] != None:
                  image['function'](*image['args'])
            elif not state[0]:
               image['is_active'] = False
         else:
            image['is_active'] = False
         
         screen.blit(image['img'], (x,y))

   def update(self, pos, state, rel, screen):
      self.draw(screen)
      self.draw_images(pos, state, screen)

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
      def __init__(self, config, gui):
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
         Region.__init__(self, *config['rect'])

         self.gui = gui
         self.builder = gui.builder

         self.path_id = ""
         self.id_info = {'method':"", 'path':""}

         self.images = []

         # Create the subsurface
         self.subsurface = pygame.Surface((self.rect[2]-2, self.rect[3]-2))
         self.subsurface_colorkey = (0,0,1)

         # Set positioning and spacing parameters
         self.scroll = 0
         self.scroll_max = 0
         self.speed = 10
         self.selected = None

      def get_images(self, config):
         self.images = []
         self.load_images(config)
         self.create_selectables(config)
         
      def set_rects(self):
         for img in self.images:
            rect = img['img'].get_rect()
            img['rect'] = pygame.Rect(self.rect.x+img['offset'][0], 
                                    self.rect.y+img['offset'][1],
                                    rect[2], rect[3])

      def load_images(self, config):
         #if config['method'] == 'spritesheet':
            # Generate batch ID
            #self.id_info['method'] = "ss"
         path_id = get_path_id(f"{self.builder.path_to_save}/config.json", config['spritesheet'])
         self.images = get_images_from_db(self.builder.database, path_id)
            #self.id_info['path'] = path_id
         
         if path_id != self.path_id:
            self.scroll = 0
         self.path_id = path_id

            #print(path_id)

            #with Image.open(config['spritesheet']) as img:
               #self.images = get_images(img)
               #self.path = config['spritesheet']

         pass
         # Pseudocode time!
         # if config['method'] == folder:
         # Load the images in the folder
         # if confi['method'] == spritesheet:
         # Load from spritesheet
         # if config[method] == listofimages:
         # Load from list of images

      def create_selectables(self, config):
         group = config['group']
         offset = config['image_start_offset']#(20,-180)
         vertical_spacing = config['vert_offset']#10
         height = offset[1]
         new_list = []

         for index, img in enumerate(self.images):
            _id = f"ss;{self.path_id};{index}"
            self.builder.add_to_db(_id, img)
            new = Selectable(img, group, hover_offset=[10,0], _id=_id)

            x = offset[0]
            y = height
            height += new.rect.height+vertical_spacing

            new.set_pos((x,y))
            new_list.append(new)

         self.images = [x for x in new_list]

         self.scroll_max = max(0, height - self.rect.height) # This has not been tested, further analysis required

      def scroll_items_select(self, pos, state):
         self.scroll = min(max(self.scroll, 0), self.scroll_max)
         
         # Prepares the subsurface for receiving the images
         self.subsurface.fill(self.subsurface_colorkey)
         self.subsurface.set_colorkey(self.subsurface_colorkey)
         self.subsurface.convert_alpha()

         for img in self.images:
            img.rect.y = img.pos[1]-self.scroll
            new_pos = (pos[0]-self.rect.x, pos[1]-self.rect.y)
            img.update(new_pos, state, self.subsurface, self.rect.collidepoint(pos))

      def scroll_event(self, event, pos):
         if self.rect.collidepoint(pos):
            self.scroll -= event.y*self.speed

      def select_selectables(self):
         select_any = False
         for img in self.images:
            if img.selected:
               select_any = True
               if not img.just_selected:
                  img.just_selected = True
                  self.builder.select(BuilderObject(img.img, img.group, img.id))
               
            else:
               img.just_selected = False
            
         if not select_any:
            if self.builder.selected != None:
               del self.builder.selected
               self.builder.select(None)

      def blit_subsurface(self, screen):
         x, y = self.rect.topleft
         screen.blit(self.subsurface, (x+1, y+1))

      def update(self, pos, state, rel, screen):
         self.draw(screen) # Inherited from Region
         self.scroll_items_select(pos, state)
         self.blit_subsurface(screen)
         self.select_selectables()

class WorldBox(Region):
   def __init__(self, config, builder):
      Region.__init__(self, *config['rect'], body_color=(0,0,0), border_color=(0,0,0))
      self.scale = 1 # Alter with scroll wheel
      self.offset = [-x for x in self.rect.center]
      self.original_offset = self.offset.copy()

      self.builder = builder

      self.scale = 1
      self.pre_scale = 1
      self.scroll_speed = 0.1
      self.scroll_min = 0.25
      self.scroll_max = 4

      self.dimensions = [1000, 1000, 1000, 1000]
      self.SIZE = config['size']
      self.is_over = False

   def draw_grid(self, screen):
      l, r, u, d = self.dimensions
      world_origin = world_to_screen((0,0), self.offset, self.scale)
      color = (200, 100, 100)

      for i in range(-l, r+1): #Draw vertical lines
         top = world_to_screen((i*self.SIZE, -u*self.SIZE), self.offset, self.scale)
         
         if top[0] < self.rect.left:
            continue
         elif top[0] > self.rect.right:
            break
            # See if this optimization actually helps at all

         bottom = world_to_screen((i*self.SIZE, d*self.SIZE), self.offset, self.scale)

         top[1] = max(self.rect.top, top[1])
         bottom[1] = min(self.rect.bottom, bottom[1])

         width = 1
         if i == 0:width = 5
         pygame.draw.line(screen, color, top, bottom, width=width)

      for i in range(-u, d+1): #Draw horizontal lines
         left = world_to_screen((-l*self.SIZE, i*self.SIZE), self.offset, self.scale)

         if left[1] < self.rect.top or left[1] > self.rect.bottom:
            # See if this optimization actually helps at all, end iteration once past limit?
            continue

         right = world_to_screen((r*self.SIZE, i*self.SIZE), self.offset, self.scale)

         left[0] = max(self.rect.left, left[0])
         right[0] = min(self.rect.right, right[0])


         width = 1
         if i == 0:width = 5
         pygame.draw.line(screen, color, left, right, width=width)

      if self.rect.collidepoint(world_origin): 
         pygame.draw.circle(screen, color, world_origin, 10)

   def pan(self, pos, rel):
      if self.rect.collidepoint(pos) and self.builder.selected == None:
         self.offset[0] -= rel[0]/self.scale
         self.offset[1] -= rel[1]/self.scale

   def scroll_event(self, event, pos):
      if self.rect.collidepoint(pos) and self.builder.can_scale:
         self.pre_scale = max(min(self.scale+event.y*self.scroll_speed, self.scroll_max), self.scroll_min)

   def get_grid_coord(self, pos):
      x, y = screen_to_world(pos, self.offset, scale=self.scale)
      return (x//self.SIZE,-y//self.SIZE)
   
   def get_screen_coord(self, world_coords):
      return world_to_screen(world_coords, self.offset, scale=self.scale)
   
   def calculate_offset(self, state, pos, rel):
      if state[0]: # and the builder has nothing selected
         self.pan(pos, rel)

      world_before_zoom = screen_to_world(pos, self.offset, self.scale)
      self.scale = self.pre_scale
      world_after_zoom = screen_to_world(pos, self.offset, self.scale)

      self.offset[0] += world_before_zoom[0] - world_after_zoom[0]
      self.offset[1] += world_before_zoom[1] - world_after_zoom[1]

   def set_grid(self, val):
      self.show_grid = val

   def draw_world(self, screen):
      m = self.builder.current_map['chunks']
      for key, chunk in m.items(): # Set to visible later, rough for now
         cx, cy = [int(x) for x in key.split(";")]
         for tile in chunk:
            if tile['group'] == 'tile':
               x, y = tile['pos']
               pos = world_to_screen(((x+cx*4)*64, (y+cy*4)*64), self.offset, self.scale) # Magic numbers!
               img = pygame.transform.scale_by(self.builder.database[tile['tile_ID']], self.scale)
               screen.blit(img, pos)
            elif tile['group'] == 'decor': # For now, identical code. However, in the future, this should include offsets for decor
               x, y = tile['pos']
               pos = world_to_screen(((x+cx*4)*64, (y+cy*4)*64), self.offset, self.scale) # Magic numbers!
               img = pygame.transform.scale_by(self.builder.database[tile['tile_ID']], self.scale)
               screen.blit(img, pos)

   def update(self, pos, state, rel, screen):
      self.draw(screen)
      self.calculate_offset(state, pos, rel)

      self.is_over = self.rect.collidepoint(pos)

      #print(self.get_grid_coord(pos))

      self.draw_world(screen)

      if self.builder.show_grid:
         self.draw_grid(screen)

class TextBox(Region):
   '''
   For optimization and practice, find a way to save the font
   to the elements to avoid repeatedly loading the text
   '''
   def __init__(self, config, builder):
      Region.__init__(self, *config['rect'])
      self.builder = builder
      self.config = config
      self.movable_text = bool(config['movable'])

      self.init_text()
      self.set_functions()

      self.selected = None
      self.horiz_shift = 10

   def init_text(self):
      self.rendered_texts = {}

      for item in self.config['text']:
         msg, pos, rect = self.render_text(item)

         func = ""
         args = []
         if 'function' in item.keys():
            func = item['function']

            args = [getattr(self, arg) for arg in item['self_args']]
            for i in item['args']:
               args.append(i)

         # Should I move this to an object? I'm repeating a lot of code in this gui system
         # Future versions should streamline functions, selectables
         self.rendered_texts[item['name']] = {'text':item['text'],'rendered_text':msg, 'pos':pos, 
                                              'anal':item['anal'], 'color':item['color'],
                                              'rect':rect, 'size':item['size'], 'active':False, 'function':func,
                                              'args':args}

   def set_functions(self):
      module = importlib.import_module("config.functions") 
      for _, txt in self.rendered_texts.items():
         if hasattr(module, txt['function']):
            function = getattr(module, txt['function'])
            txt['function'] = function
         else:
            if txt['function'] != "":
               print(f"Function {txt['function']} not found")
            txt['function'] = None

   def draw_text(self, pos, state, screen):
      already_hovering = False
      for key, i in self.rendered_texts.items():
         x, y = i['pos']
         if not already_hovering:
            if i['rect'].collidepoint(pos):
               already_hovering = True
               if self.movable_text: x += self.horiz_shift
               if state[0] and self.selected != i:
                  self.selected = i
                  if i['function'] != None:
                     i["function"](*i['args'])
   
         screen.blit(i['rendered_text'], (x,y))

   def render_text(self, item):
      font = pygame.font.Font("pynamogui/data/at01.ttf", item['size'])
      msg = font.render(str(item['text']), item['anal'], item['color'])
      pos = (item['pos'][0]+self.rect.x,
                item['pos'][1]+self.rect.y)
      rect = msg.get_rect(x=pos[0], y=pos[1])

      return msg, pos, rect


   def add_text(self, text, size, color, pos, name, anal=False):
      font = pygame.font.Font("pynamogui/data/at01.ttf", size)
      msg = font.render(text, anal, color)
      pos = (pos[0]+self.rect.x,
             pos[1]+self.rect.y)
      rect = msg.get_rect(x=pos[0], y=pos[1])
      self.rendered_texts[name] = {'text':text, 'rendered_text':msg, 'pos':pos, 
                                   'size':size,'anal':anal,'color':color,
                                   'rect':rect, 'active':False, 'function':""}

   def modify_text(self, txt_name, value):
      """
      Currently only modifies the text value
      """
      item = self.rendered_texts[txt_name]
      item['text'] = value

      msg, pos, rect = self.render_text(item)
      item['rendered_text'] = msg
      item['rect'] = rect


   def update(self, pos, state, rel, screen):
      self.draw(screen)
      self.draw_text(pos, state, screen)

class FolderNav(Region):
   def __init__(self, config, gui):
      Region.__init__(self, *config['rect'])

      self.gui = gui

      self.cwd = os.getcwd()
      self.dir = config['dir']

   def get_items(self):
      print(os.listdir(f"{self.cwd}/{self.dir}"))

   def create_cells(self):
      pass

   def update(self, pos, state, rel, screen):
      self.draw(screen)

      if state[0]:
         self.get_items()