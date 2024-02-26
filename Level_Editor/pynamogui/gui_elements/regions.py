import pygame
import json
import importlib
import os
import functools

from PIL import Image

from ..misc.core_functions import get_asset_files, world_to_screen, screen_to_world, load_json, prep_image, get_images, screen_to_chunk, screen_to_chunk_id
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
      
      print(self.images)

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
            img['use_args'] = args

         else:
            print(f"Function {img['function']} not found")
            img['function'] = None

   def update_args(self):
      def rgetattr(obj, attr, *args):
         def _getattr(obj, attr):
            return getattr(obj, attr, *args)
         return functools.reduce(_getattr, [obj] + attr.split('.'))
      
      for img in self.images:
         args = [rgetattr(self, arg) for arg in img['self_args']]
         for i in img['args']:
            args.append(i)
         img['use_args'] = args




   def draw_images(self, pos, state, screen):
      for image in self.images:
         x, y = image['rect'].topleft
         if image['rect'].collidepoint(pos):
            if self.movable:
               y -= 5
            if state[0] and not image['is_active']:
               image['is_active'] = True
               if image['function'] != None:
                  self.update_args() #ugly code
                  image['function'](*image['use_args'])
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

         self.get_images(config)

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

      def create_selectables(self, config):
         group = config['group']
         offset = (10,10)#config['image_start_offset']#(20,-180)
         vertical_spacing = 10 #config['vert_offset']#10
         height = offset[1]
         new_list = []

         for index, img in enumerate(self.images):
            _id = f"ss;{self.path_id};{index}"
            self.builder.add_to_db(_id, img)
            new = Selectable(img, group, hover_offset=[10,0], _id=_id, autotilable=bool(config['auto?']))

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
                  self.builder.select(BuilderObject(img.img, img.group, img.id, img.autotilable))
               
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

      self.chunk_size = 4

      self.scale = 1
      self.pre_scale = 1
      self.scroll_speed = 0.1
      self.scroll_min = 0.125/2
      self.scroll_max = 4

      self.dimensions = [1000, 1000, 1000, 1000]
      self.SIZE = config['size']
      self.is_over = False

      self.load_trigger_surface()

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
      return (int(x//self.SIZE),int(y//self.SIZE))
   
   def get_chunk_from_grid(self, tile_pos):
      x, y = tile_pos
      chunk_id = f"{int(x//4)};{int(y//4)}"
      return chunk_id

   def get_screen_coord(self, world_coords):
      return world_to_screen(world_coords, self.offset, scale=self.scale)
   
   def get_tile_coord(self, pos):
      # cx, cy describes the x- and y-coordinate of the active chunk
      cx, cy = screen_to_chunk(pos, self.offset, self.scale)

      # px, py decribes the coordinate of the square within the chunk
      px, py = self.get_grid_coord(pos)
      tile_pos = [int(px%4), int(py%4)]
      chunk_id = f"{cx};{cy}"

      return tile_pos, chunk_id

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

   def load_trigger_surface(self):
      size = 64
      self.trigger = pygame.Surface((size,size))
      pygame.draw.rect(self.trigger, (20,240,120), (0,0,size,size))

   def draw_world(self, screen):
      # Get the current world
      m = self.builder.current_map['chunks']

      renderer = []

      # IDEA:
      # Check to see what chunks are on screen
      # Then, pass all tiles to a render list and sort with z-order
      # Once that's done, only check to see if a chunk is loaded or unloaded,
      # eliminating the need to recalculate every frame

      ax, ay = screen_to_chunk(self.rect.topleft, self.offset, scale=self.scale)
      bx, by = screen_to_chunk(self.rect.bottomright, self.offset, scale=self.scale)

      c_dx = bx-ax+1 # +1 adds a bit of buffer for seamless drawing
      c_dy = by-ay+1
      
      chunk_map = []
   
      for x in range(-1, c_dx):
         for y in range(-1, c_dy):
               chunk_map.append(f"{ax+x};{ay+y}")
                  
      # For each item in the world
      for key, chunk in m.items(): # Set to visible later, rough for now

         if key in chunk_map:

            # Convert chunk id into usable parameters
            cx, cy = [int(x) for x in key.split(";")]

            # Pass all tiles in chunk to a renderer
            for tile in chunk:

               # Draw tiles
               if tile['group'] == 'tile':
                  x, y = tile['pos']
                  pos = world_to_screen(((x+cx*4)*64, (y+cy*4)*64), self.offset, self.scale) # Magic numbers!

                  pos = [p + tile['offset'][i]*self.scale for i, p in enumerate(pos)]

                  img = pygame.transform.scale_by(self.builder.database[tile['tile_ID']], self.scale)
                  renderer.append((img, pos, tile["z-order"]))

               elif tile['group'] == 'decor': # For now, identical code. However, in the future, this should include offsets for decor

                  if tile["offset"] == [0,0]:
                     x, y = tile['pos']
                     pos = world_to_screen(((x+cx*4)*64, (y+cy*4)*64), self.offset, self.scale) # Magic numbers!

                  else:
                     x, y = tile['offset']
                     pos = world_to_screen((x, y), self.offset, self.scale) # Magic numbers!

                  img = pygame.transform.scale_by(self.builder.database[tile['tile_ID']], self.scale)
                  screen.blit(img, pos)

               if tile['group'] == 'trigger' and self.builder.show_trigger:
                  x, y = tile['pos']
                  pos = world_to_screen(((x+cx*4)*64, (y+cy*4)*64), self.offset, self.scale) # Magic numbers!

                  pos = [p + tile['offset'][i]*self.scale for i, p in enumerate(pos)]

                  img = pygame.transform.scale_by(self.trigger, self.scale)
                  renderer.append((img, pos, tile["z-order"]))
         
      for item in sorted(renderer, key=lambda x:(x[2], x[1][1])): # sort based on z-order
         screen.blit(item[0], item[1])

   def place_asset(self, pos, layer, selected, current_map, snap_to=False):
      # cx, cy describes the x- and y-coordinate of the active chunk
      cx, cy = screen_to_chunk(pos, self.offset, self.scale)

      # px, py decribes the coordinate of the square within the chunk
      px, py = self.get_grid_coord(pos)

      # px makes sense for now, but py is a mystery
      px = int(px%4)
      py = int(py%4)

      # Code for freeform placement
      mx, my = 0,0
      if not snap_to:
         mx, my = screen_to_world(pos, self.offset, scale=self.scale)
         mx, my = int(mx), int(my)

      # Create and place new object reference - doesn't need to be over-optimized
      new_obj = {"tile_ID":selected.id, "group":selected.group,
                  "z-order":layer,"pos":[px, py], "offset":[mx,my],
                  "sum":0, "auto?":int(selected.autotilable)}

      chunk_id = f"{cx};{cy}"

      # Clear the map for new asset
      self.remove_asset(new_obj['pos'], new_obj['z-order'], chunk_id, current_map)

      current_map['chunks'][chunk_id].append(new_obj)

   def place_asset_by_coord(self, chunk_id, tile_pos, layer, group, id_, current_map, snap_to=False, offset=[0,0], auto=False):

      # Create and place new object reference - doesn't need to be over-optimized
      new_obj = {"tile_ID":id_, "group":group,
                  "z-order":layer,"pos":tile_pos, "offset":[x*self.chunk_size for x in offset],
                  "sum":0,"auto?":int(auto)}
      
      # Clear the map for new asset
      self.remove_asset(new_obj['pos'], new_obj['z-order'], chunk_id, current_map)

      current_map['chunks'][chunk_id].append(new_obj)

   def remove_asset(self, obj_pos, obj_layer, chunk_id, current_map):
      if chunk_id not in current_map['chunks']:
         current_map['chunks'][chunk_id] = []

      for i in current_map['chunks'][chunk_id]:
         if i["pos"] == obj_pos and i['z-order'] == obj_layer:
               current_map['chunks'][chunk_id].remove(i)
               break      

   def get_at(self, tile_pos, chunk_id, layer, current_map):
      if chunk_id in current_map['chunks']:
         chunk = current_map['chunks'][chunk_id]
         for tile in chunk:
            if tile['pos'] == tile_pos and tile['z-order'] == layer:
               return tile
      return None
      
   def get_neighbors(self, tile_pos, chunk_id):

      def concat_chunk(x, y):
         return f"{x};{y}"
      # chunk_id is given as the hash key in the form "1;2"
      # tile is given as [0,3]
      # given neighbors in the form of a dictionary
      # i.e. {"1;2":[0,3], "2;2"[0,1]}]
      cardinal_neighbors = []
      diagonal_neighbors = []
      cx, cy = [int(c) for c in chunk_id.split(";")]
      x, y = tile_pos

      up_chunk = f"{cy - (not y)}"
      down_chunk = f"{cy + y//(self.chunk_size-1)}" #schniesty code, but it works, I guess
      right_chunk = f"{cx + x//(self.chunk_size-1)}"
      left_chunk = f"{cx - (not x)}"

      lx = (x-1)%self.chunk_size # left x tile pos
      rx = (x+1)%self.chunk_size
      uy = (y-1)%self.chunk_size # up y
      dy = (y+1)%self.chunk_size

      # Up
      cardinal_neighbors.append([concat_chunk(cx, up_chunk),[x, uy], "up"])

      # Then the right
      cardinal_neighbors.append([concat_chunk(right_chunk, cy),[rx, y], "right"])
 
      # Down
      cardinal_neighbors.append([concat_chunk(cx, down_chunk),[x, dy], "down"])

      # Left
      cardinal_neighbors.append([concat_chunk(left_chunk, cy),[lx, y], "left"])

      # upright
      diagonal_neighbors.append([concat_chunk(right_chunk, up_chunk),[rx, uy], "up-right"])

      # down right
      diagonal_neighbors.append([concat_chunk(right_chunk, down_chunk),[rx, dy], "down-right"])

      # up left
      diagonal_neighbors.append([concat_chunk(left_chunk, up_chunk),[lx, uy], "up-left"])

      # down left
      diagonal_neighbors.append([concat_chunk(left_chunk, down_chunk),[lx, dy], "down-left"])

      return cardinal_neighbors, diagonal_neighbors

   def get_range(self, pos1, pos2):
      p1 = self.get_grid_coord(pos1)
      p2 = self.get_grid_coord(pos2)

      topleft = [int(min(p1[0], p2[0])), int(max(p1[1], p2[1]))]
      botright = [int(max(p1[0], p2[0])), int(min(p1[1], p2[1]))]

      return topleft, botright
   
   def get_range_from_tile(self, pos, radius=4):
      wx, wy = screen_to_world(pos, self.offset, self.scale)

      tx, ty = int(wx//64), int(wy//64)
      
      tiles = []
      for x in range(tx-radius, tx+radius + 1):
         for y in range(ty-radius, ty+radius+1):
            tile_pos = [self.get_chunk_from_grid((x,y)),[x%4,y%4]]
            tiles.append(tile_pos)

      #print(tiles)
      return tiles

   def get_tiles_in_range(self, tl, br):
      c1 = self.get_chunk_from_grid(tl)
      c2 = self.get_chunk_from_grid(br)

   def update(self, pos, state, rel, screen):
      if self.visible:
         self.draw(screen)
         self.calculate_offset(state, pos, rel)

         self.is_over = self.rect.collidepoint(pos)

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

class StaticSelectBox(Region):
   # To be uised for tilesets (autotile)
   # So, this thing is going to need:
   # 1) Some sort of access to tilesets to get the display image
   # 2) Interactive tile movements (slide right on hover)
   # 3) Connection to autotile algorithm

   def __init__(self, config, gui):
      Region.__init__(self, *config['rect'])

      self.gui = gui
      self.builder = gui.builder

      self.offset = [10,10]
      self.vert_spacing = 10

      self.images = self.load_images(config)
      self.disp_image = Selectable(self.images[-1], "tile", [10,0], _id = f"ss;{self.path_id};{48}")
      self.disp_image.set_pos((self.rect.x + self.offset[0], self.rect.y + self.offset[1]))
      self.selectables = [self.disp_image]

   def load_images(self, config):
      self.path_id = get_path_id(f"{self.builder.path_to_save}/config.json", config['spritesheet'])
      return get_images_from_db(self.builder.database, self.path_id)
   
   def draw_selectables(self, pos, state, screen):
      self.disp_image.update(pos, state, screen, True)

   def select_selectables(self):
      select_any = False
      for img in self.selectables:
         if img.selected:
            select_any = True
            if not img.just_selected:
               img.just_selected = True
               self.builder.select(BuilderObject(img.img, img.group, img.id, autotilable=True))
            
         else:
            img.just_selected = False
         
      if not select_any:
         if self.builder.selected != None:
            del self.builder.selected
            self.builder.select(None)

   def update(self, pos, state, rel, screen):
      self.draw(screen)
      self.draw_selectables(pos, state, screen)
      self.select_selectables()

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

class TriggerBox(Region):
   def __init__(self, config, gui):
      Region.__init__(self, *config['rect'])

      self.gui = gui
      self.builder = gui.builder

      self.offset = [10,10]
      self.vert_spacing = 10

      self.text = ""
      self.font = pygame.font.Font(None, 32) 


      size = 64
      self.img = pygame.Surface((size,size))
      pygame.draw.rect(self.img, (20,240,120), (0,0,size,size))
      self.disp_image = Selectable(self.img, "trigger", [10,0])
      self.disp_image.set_pos([10,10])

   def draw_symbol(self, pos, state, screen):
      self.disp_image.update(pos, state, screen, True)

   def handle_text(self, event):
      if event.key == pygame.K_BACKSPACE: 
         # get text input from 0 to -1 i.e. end. 
         self.text = self.text[:-1] 

      # Unicode standard is used for string 
      # formation 
         
      elif event.key == pygame.K_RETURN: 
         # get text input from 0 to -1 i.e. end. 
         self.disp_image.set_id(self.text)
      elif event.key == pygame.K_DELETE: 
         # get text input from 0 to -1 i.e. end. 
         self.text = ""
         self.disp_image.set_id(self.text)
      else: 
         self.text += event.unicode

   def clear_text(self):
      self.text = ""

   def select_selectables(self):
      select_any = False
      if self.disp_image.selected:
         select_any = True
         if not self.disp_image.just_selected:
            self.disp_image.just_selected = True
            self.builder.select(BuilderObject(self.disp_image.img, self.disp_image.group, 
                                                         self.disp_image.id, autotilable=False))
         
      else:
         self.disp_image.just_selected = False
         
      if not select_any:
         if self.builder.selected != None:
            del self.builder.selected
            self.builder.select(None)

   def draw_text_display(self, screen):
      pygame.draw.rect(screen, (50, 125, 168), (10,100, 150,30))
      txt = self.font.render(self.text, True, (255, 255, 255))
      screen.blit(txt, (15,105))

   def __str__(self):
      return "trigger"

   def update(self, pos, state, rel, screen):
      self.draw(screen)
      self.select_selectables()
      self.draw_symbol(pos, state, screen)
      self.draw_text_display(screen)

      #print(self.text)