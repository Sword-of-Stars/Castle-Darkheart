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

    Future Work
    ------------
    Generalize to allow any header type to be used

   """
   def __init__(self, rect, path):
      Region.__init__(self, *rect)
      self.path = path

      #-- Render folder names --#
      text_spacing = 30
      text_pos = (10,0)
      self.lst = get_asset_files(f"{path}/data")
      self.names = {x:{
                  "pos":(text_pos[0],text_pos[1]+text_spacing*index),
                  "text":draw_text(x, (255,255,255), font),
                  "rect":None}
                  for index, x in enumerate(self.lst)}
      for name in self.names:
         self.names[name]["rect"] = self.names[name]["text"].get_rect()
         self.names[name]["rect"].x, self.names[name]["rect"].y, = self.names[name]["pos"]

      self.selected_folder = None

   def draw_text(self, pos, state, screen):
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
      def __init__(self, config, builder):
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

         self.builder = builder

         self.images = None
         self.load_images(config)
         #self.prepare_images(config)
         self.create_selectables(config)

         # Create the subsurface
         self.subsurface = pygame.Surface((self.rect[2]-2, self.rect[3]-2))
         self.subsurface_colorkey = (0,0,1)

         # Set positioning and spacing parameters
         self.scroll = 0
         self.speed = 10
         self.selected = None

      def do_images(self):
         new_imgs = []
         for img in self.images:
            selectable_image = Selectable(img, (self.rect.x+img['offset'][0], 
                                    self.rect.y+img['offset'][1]), [10,0])
            new_imgs.append[selectable_image]

      def set_rects(self):
         for img in self.images:
            rect = img['img'].get_rect()
            img['rect'] = pygame.Rect(self.rect.x+img['offset'][0], 
                                    self.rect.y+img['offset'][1],
                                    rect[2], rect[3])

      def load_images(self, config):
         if config['method'] == 'spritesheet':
            with Image.open(config['spritesheet']) as img:
               self.images = get_images(img)
         pass
         # Pseudocode time!
         # if config['method'] == folder:
         # Load the images in the folder
         # if confi['method'] == spritesheet:
         # Load from spritesheet
         # if config[method] == listofimages:
         # Load from list of images

      def create_selectables(self, config):
         offset = config['image_start_offset']#(20,-180)
         vertical_spacing = config['vert_offset']#10
         height = 0
         new_list = []

         self.images = [prep_image(x, config['scale'], config['colorkey']) for x in self.images]         

         for img in self.images:
            new = Selectable(img, [10,0])
            x = offset[0]
            y = height+offset[1]
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
            img.update(new_pos, state, self.subsurface)

      def prepare_images2(self, config):
         offset = config['image_start_offset']#(20,-180)
         vertical_spacing = config['vert_offset']#10
          # Load images and relevant information in dictionary
         self.images = [{'img':prep_image(x, config['scale'], config['colorkey'])} for x in self.images]         
         # Store the image rect values and positions in the self.images dict
         height = 0
         for image in self.images:
            rect = image['img'].get_rect()
            x = offset[0]
            y = height+offset[1]
            height += image['rect'].height+vertical_spacing

            image['rect'].topleft = x, y # Yeah, pretty sure this won't work
            image['pos'] = [x,y]
            image['isover'] = False
         
         self.scroll_max = max(0, height - self.rect.height) # This has not been tested, further analysis required

      def prepare_images(self, config):
         offset = config['image_start_offset']#(20,-180)
         vertical_spacing = config['vert_offset']#10
          # Load images and relevant information in dictionary
         self.images = [{'img':prep_image(x, config['scale'], config['colorkey'])} for x in self.images]         
         # Store the image rect values and positions in the self.images dict
         height = 0
         for image in self.images:
            image['rect'] = image['img'].get_rect()
            x = offset[0]
            y = height+offset[1]
            height += image['rect'].height+vertical_spacing

            image['rect'].topleft = x, y # Yeah, pretty sure this won't work
            image['pos'] = [x,y]
            image['isover'] = False
         
         self.scroll_max = max(0, height - self.rect.height) # This has not been tested, further analysis required

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
         for img in self.images:
            img["rect"].y = img["pos"][1]-self.scroll

            if img["isover"]:
                  x = img["pos"][0]+10
            else:
                  x = img["pos"][0]

            self.subsurface.blit(img["img"], (x, img["rect"].y))

      def select_selectables(self):
         for img in self.images:
            if img.selected and not img.just_selected:
               self.builder.select(BuilderObject(img.img))
               break
         else:
            del self.builder.selected
            self.builder.select(None)

      def select(self, pos, state):
         if self.rect.collidepoint(pos): # If the mouse is over the scroll box
            # Change mouse pos to accomodate for positional differences
            x, y = pos
            x -= self.rect.x
            y -= self.rect.y
            for img in self.images:
                  if img["rect"].collidepoint((x,y)):
                     img["isover"] = True
                     if state[0]:
                        self.selected = img
                        self.builder.select(img)
                  else:
                     img["isover"] = False

         if state[2]:
            self.selected = None

      def blit_subsurface(self, screen):
         x, y = self.rect.topleft
         screen.blit(self.subsurface, (x+1, y+1))

      def update(self, pos, state, rel, screen):
         #self.select(pos, state)
         self.draw(screen) # Inherited from Region
         self.scroll_items_select(pos, state)
         self.blit_subsurface(screen)
         self.select_selectables()