import pygame

from ..gui_elements.region import Region
from ..misc.core_functions import prep_image2, set_function, render_text

class Button(Region):
    def __init__(self, rect, text, body_color1=(19, 46, 66), body_color2=(80,46,66), 
                 border_color=(113, 144, 227), border_width=1, 
                 font=None, font_size=20, font_color=(255,255,255), func=print):
        Region.__init__(self, *rect, body_color1, border_color, border_width)

        self.body_color = body_color1
        self.body_color1 = body_color1
        self.body_color2 = body_color2

        # Begin: Initialize and prepare font
        self.font_size = font_size
        self.font_color = font_color
        self.font = font
        if self.font == None:
            self.font = pygame.font.Font("pynamogui/data/at01.ttf", self.font_size)
        self.render_text(text)
        # End: Initialize and prepare font

        self.is_over = False
        self.func = func #Maybe use lambda and other methods to complete function

    def render_text(self, text, color=None):
        if color == None:
            color = self.font_color
        self.text = self.font.render(text, False, color)

    def check_is_over(self, pos):
        self.is_over = self.rect.collidepoint(pos)
        return self.is_over
    
    def check_if_clicked(self, state):
        if self.is_over:
            if state[0]:
                print("Yep, it's clicked") # replace with function eventually
    
    def swap_color(self):
        if self.is_over:
            self.body_color = self.body_color1
        else:
            self.body_color = self.body_color2

    def update(self, pos, state, rel, screen):
        self.check_is_over(pos)
        self.swap_color()
        self.check_if_clicked(state)
        self.draw(screen)

class ImgButton():
    def __init__(self, image, pos, border_color=(113, 144, 227), border_width=0, 
                 font=None, font_size=20, font_color=(255,255,255), move=[0,-5],
                 func=print):
        self.img = image #pygame.image.load(image).convert_alpha()
        self.rect = self.img.get_rect(x=pos[0], y=pos[1])
        self.pos = pos
        self.border_rect = pygame.rect.Rect(self.rect.x-border_width, self.rect.y-border_width, 
                                    self.rect.width+2*border_width, self.rect.height+2*border_width)
        
        self.is_over = False
        self.func = func #Maybe use lambda and other methods to complete function
        self.move_on_hover = move

    def check_is_over(self, pos):
        self.is_over = self.rect.collidepoint(pos)
        return self.is_over
    
    def move(self):
        if self.is_over:
            self.rect.x = self.pos[0] + self.move_on_hover[0]
            self.rect.y = self.pos[1] + self.move_on_hover[1]
    
    def check_if_clicked(self, state):
        if self.is_over:
            if state[0]:
                print("Yep, it's clicked, image")

    def display_image(self, screen):
        screen.blit(self.img, self.rect.topleft)

    def update(self, pos, state, rel, screen):
        self.check_is_over(pos)
        self.move()
        self.check_if_clicked(state)
        self.display_image(screen)

class ImgButton_base(Region):
    def __init__(self, config, gui, border_color=(113, 144, 227), border_width=1, 
                 font=None, font_size=20, font_color=(255,255,255), move=[0,0]):
        
        self.border_width = border_width
        self.gui = gui
        self.builder = gui.builder
        self.img = prep_image2(config['image'], config['scale'])
        self.pos = config['pos']

        img_padding = config['img_pad']

        self.img_rect = self.img.get_rect(x=self.pos[0], y=self.pos[1])
        box_rect = (self.pos[0]-img_padding, self.pos[1]-img_padding, 
                    self.img_rect.width+2*img_padding, self.img_rect.height+2*img_padding)

        Region.__init__(self, *box_rect, border_width=border_width)

        self.is_over = False

        # Absolutely Sh*t code, but good enough for now
        self.func = set_function(config['function']) #Maybe use lambda and other methods to complete function
        self.args = [getattr(self, arg) for arg in config['self_args']]
        for i in config['args']:
            self.args.append(i)

        self.move_on_hover = move
        self.just_selected = True

        self.color_1 = self.body_color
        self.color_2 = (31, 69, 97)

    def check_is_over(self, pos):
        self.is_over = self.rect.collidepoint(pos)
        return self.is_over
        
    def swap_color(self):
        if self.is_over:
            self.body_color = self.color_2
        else:
            self.body_color = self.color_1
    
    def move(self):
        if self.is_over:
            self.img_rect.x = self.pos[0] + self.move_on_hover[0]
            self.img_rect.y = self.pos[1] + self.move_on_hover[1]
        else:
            self.img_rect.topleft = self.pos
    
    def check_if_clicked(self, state):
        if self.is_over:
            if state[0] and not self.just_selected:
                self.just_selected = True
                self.gui.builder.select(None)
                self.func(*self.args)
            elif not state[0]:
                self.just_selected = False
        else:
            self.just_selected = False

    def display_image(self, screen):
        screen.blit(self.img, self.img_rect.topleft)

    def update(self, pos, state, rel, screen):
        self.check_is_over(pos)
        self.swap_color()
        self.move()
        self.check_if_clicked(state)
        self.draw(screen)
        self.display_image(screen)

class BuilderObject():
    """
    Contains all necessary information to display an image to the screen 
    and create the map build file
    """
    def __init__(self, img, group, _id=""):
        self.id = _id
        self.group = group
        self.img = img.copy()
        self.img.set_alpha(128)
        self.disp_image = self.img.copy()
        self.rect = img.get_rect()

        #print(f"ID: {self.id}")

    def scale(self, scale):
        self.disp_image = pygame.transform.scale_by(self.img, scale)
        self.rect = self.disp_image.get_rect()

    def set_pos(self, pos):
        self.rect.center = pos

    def update(self, screen):
        screen.blit(self.disp_image, self.rect.topleft)

class Selectable():
    def __init__(self, img, group, hover_offset=[0,0], _id="", ):
        self.id = _id
        self.img = img
        self.group = group

        self.rect = img.get_rect()
        self.orig_rect = self.rect.copy()

        self.pos = [0,0]
        self.selected = False
        self.just_selected = False
        self.isover = False
        self.hover_offset = hover_offset

    def show_rect(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

    def set_pos(self, pos):
        self.pos = pos
        self.rect.topleft = pos

    def is_over(self, pos, over_region):
        if self.rect.collidepoint(pos) and over_region:
            self.isover = True
        else:
            self.isover = False
        return self.isover
    
    def is_selected(self, state):
        if self.isover:
            if state[0]:
                self.selected = True
        else:
            if not self.selected:
                self.isover = False

        if state[2]:
            self.selected = False

    def unselect(self):
        self.selected = False
    
    def draw(self, surf):
        x, y = self.rect.topleft
        if self.isover:
            x += self.hover_offset[0]
            y += self.hover_offset[1]
        surf.blit(self.img, (x,y))

    def update(self, pos, state, surf, is_over_region):
        self.is_over(pos, is_over_region)
        self.is_selected(state)
        self.draw(surf)

class SelectableCell():
    def __init__(self, rect, img, text):
        self.rect = rect
        self.img = img
        self.text = text

        self.is_over = False
        self.selected = False
        self.just_selected = False
        
        self.color_1 = (19, 46, 66)
        self.color_2 = (17, 67, 105)
        self.color_3 = (5, 92, 158)
        self.color = self.color_1

    def check_is_over(self, pos):
        if self.rect.collidepoint(pos):
            self.is_over = True
            if not self.selected: self.color = self.color_2

    def check_selected(self, state):
        if self.is_over:
            if state[0]:
                if not self.just_selected:
                    self.selected = True
                    self.just_selected = True
                    self.color = self.color_3
        if state[2]:
            self.just_selected = False
            self.selected = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def update(self, screen, pos, state):
        self.check_is_over(pos)
        self.check_selected(state)
        self.draw(screen)

class Checkbox(Region):
    def __init__(self, config, gui):
        Region.__init__(self, *config['rect'], body_color=(135, 132, 145), border_color=(25, 24, 26))

        self.gui = gui
        self.builder = gui.builder

        self.color_1 = self.body_color
        self.color_2 = (148, 144, 153)

        #self.active = bool(config['default'])

        self.pos = config['pos']
        self.img = prep_image2("data/check.png", config['scale'])
        self.img_rect = self.img.get_rect(x=self.rect.x+self.pos[0], y=self.rect.y+self.pos[1])

        self.text, self.txt_pos, _ = self.render_text(config['text'])

        self.mod_attr = config['attr']
        self.active = getattr(self.builder, self.mod_attr)


    def render_text(self, config):
        font = pygame.font.Font("pynamogui/data/at01.ttf", config['size'])
        msg = font.render(str(config['text']), config['anal'], config['color'])
        pos = (config['pos'][0]+self.rect.x,
                config['pos'][1]+self.rect.y)
        rect = msg.get_rect(x=pos[0], y=pos[1])

        return msg, pos, rect

    def check_is_over(self, pos):
        self.is_over = self.rect.collidepoint(pos)
        return self.is_over
        
    def swap_color(self):
        if self.is_over:
            self.body_color = self.color_2
        else:
            self.body_color = self.color_1

    def draw_text(self, screen):
        pass

    def toggle(self):
        self.active = not self.active
        setattr(self.builder, self.mod_attr, self.active)
    
    def check_if_clicked(self, state):
        if self.is_over:
            if state[0] and not self.just_selected:
                self.just_selected = True
                self.toggle()
                
            elif not state[0]:
                self.just_selected = False
        else:
            self.just_selected = False

    def display_image(self, screen):
        if self.active:
            screen.blit(self.img, self.img_rect.topleft)

    def display_text(self, screen):
        screen.blit(self.text, self.txt_pos)

    def update(self, pos, state, rel, screen):
        self.check_is_over(pos)
        self.swap_color()
        self.check_if_clicked(state)
        self.draw(screen)
        self.display_image(screen)
        self.display_text(screen)

