import pygame

def draw_text(msg, color, font):
    return font.render(msg, False, color)

def prep_image(img, scale, colorkey=(255,255,255), return_rect=False):
      rect = img.get_rect()
      img = pygame.transform.scale(img, (rect.width*scale, rect.height*scale))
      img.set_colorkey(colorkey)
      if return_rect:
        return img, img.get_rect()
      return img

def load_pixel_image(file_name, colorkey=(255,255,255), scale=4):
    img = pygame.image.load(file_name).convert_alpha()
    img.set_colorkey(colorkey)
    img = pygame.transform.scale(img, [x*scale for x in img.get_size()]).convert_alpha()
    return img

def scale_pixel_image(img, colorkey=(255,255,255), scale=4):
    img.set_colorkey(colorkey)
    img = pygame.transform.scale(img, [x*scale for x in img.get_size()]).convert_alpha()
    return img