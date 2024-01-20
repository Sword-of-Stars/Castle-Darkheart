import pygame

class Region():
   """
   Defines a colored region with a border on which elements are displayed

   Methods
   -------
   draw
      draws the region and its border
   update
      displays the region on the screen 
   """
   def __init__(self, x, y, width, height, body_color=(19, 46, 66), border_color=(113, 144, 227), border_width=1):
      self.border_rect = pygame.rect.Rect(x, y, width, height)
      self.rect = pygame.rect.Rect(x+border_width, y+border_width, 
                                   width-2*border_width, height-2*border_width)
      
      self.body_color = body_color
      self.border_color = border_color

      self.visible = True

   def draw(self, screen):
      pygame.draw.rect(screen, self.border_color, self.border_rect)
      pygame.draw.rect(screen, self.body_color, self.rect)

   def scroll_event(self, event, pos):
      pass

   def update(self, pos, state, rel, screen):
      if self.visible:
         self.draw(screen)
