import pygame, sys, os
import math

pygame.init()
WIDTH, HEIGHT = 800,600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Region():
   def __init__(self, x, y, width, height):
      self.border_rect = pygame.rect.Rect(x, y, width, height)
      border_width = 1
      self.rect = pygame.rect.Rect(x+border_width, y+border_width, 
                                    width-2*border_width, height-2*border_width)
      
      self.body_color = (19, 46, 66)
      self.border_color = (113, 144, 227)

   def draw(self):
      pygame.draw.rect(screen, self.border_color, self.border_rect)
      pygame.draw.rect(screen, self.body_color, self.rect)

   def update(self, pos, state):
      self.draw()

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
    def __init__(self, rect, orientation="linear"):
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
        self.subsurface = pygame.Surface((rect[2], rect[3]))
        self.subsurface_colorkey = (0,0,1)

        # Set positioning and spacing parameters
        offset = (-10,10)
        vertical_spacing = 60
        self.scroll = 0

        # Load images and relevant information in dictionary
        self.images = {i:
                       {"img":pygame.image.load("editor/lab/load.png").convert_alpha()} 
                       for i in range(5)}
        
        # Store the image rect values and positions in the self.images dict
        for index, name in enumerate(self.images):
            x = self.rect.x+offset[0]
            y = self.rect.y+vertical_spacing*(index-1)+offset[1]

            rect = self.images[name]["img"].get_rect(x=x, y=y)
            self.images[name]["pos"] = (x, y)
            self.images[name]["rect"] = rect
            self.images[name]["selected"] = False        

        # Calculate the max spacing by summing heights and vertical spacing
        # NOTE: There's a much better way to do this
        img_heights = 0
        for _, img in self.images.items():
            rect = img["img"].get_rect()
            img_heights += rect.height+vertical_spacing
        self.scroll_max = img_heights - self.rect.height


    def scroll_event(self, event):
        s.scroll += event.y

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

            if img["selected"]:
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
                    img["selected"] = True
                    self.selected = img
                else:
                    img["selected"] = False

    def update(self):
        self.draw() # Inherited from Region
        self.scroll_items() 
        screen.blit(self.subsurface, self.rect.topleft)

s = ScrollBox((30,70,300,300))
      
while True:
    screen.fill((0,0,0))
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEWHEEL:
            s.scroll_event(event)

    s.select(pygame.mouse.get_pos(), pygame.mouse.get_pressed())
    s.update()

    pygame.display.update()