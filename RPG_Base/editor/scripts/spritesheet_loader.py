import pygame, sys, os
from tkinter import *
from tkinter import filedialog


pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spritesheet Separator v1.0")
clock = pygame.time.Clock()

#########################
# Initializing Varibles #
#########################
COLORKEY = (0,0,0)


#############
# Functions #
#############

def scale_image(img, width, height):
    imgw, imgh = img.get_size()
    scalex = width/imgw
    scaley = height/imgh

    if scalex < 1 or scaley < 1: #if the image size is larger than the designated width and height
        scale_factor = min(scalex, scaley)
        new_size = (scale_factor*imgw, scale_factor*imgh)
        return pygame.transform.scale(img, new_size).convert_alpha()
    return img

def browseFiles(path):
    folder_path = filedialog.askdirectory(initialdir = path,
										title = "Select a Folder")
    return folder_path

def parse_path(path, num=3):
    elements = path.split("/")

    short_path = elements[len(elements)-num:]
    final_path = "/".join(short_path)
    return final_path

def kick_off_actual_functionality(file_manager, settings):
    files = file_manager.get_selected_files()
    stitch = settings.ui_elements["stitch"].selected
    print(files, stitch)

###########
# Classes #
###########

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
    
class Button(Region):
    def __init__(self, rect, text, color1=(150, 150, 150), color2=(120, 120, 120), on_click=None, parent=None):
        Region.__init__(self, *rect)

        self.text = font.render(text, False, (255, 255, 255))
        self.selected = False
        self.just_pressed = False


        self.color1 = color1
        self.body_color = self.color1
        self.border_color = (0,0,0)
        self.color2 = color2

        self.on_click = on_click
        self.parent = parent

    def is_over(self, state, pos):
        if self.rect.collidepoint(pos):
            self.body_color = self.color2
            if state[0] and not self.just_pressed:
                self.just_pressed = True
                self.selected = True
                if self.on_click == browseFiles:
                    new_dir = self.on_click(self.parent.path)
                    if new_dir != "":
                        self.parent.update_path(new_dir)
                elif self.on_click != None:
                    kick_off_actual_functionality(self.parent[0], self.parent[1])
            elif not state[0]:
                self.just_pressed = False
                    
        else:
            self.body_color = self.color1

    def draw_text(self):
        x, y = self.rect.topleft
        screen.blit(self.text, (x+10, y-3))

    def update(self, state, pos):
        self.is_over(state, pos)
        self.draw()
        self.draw_text()

class Checkbox(Region):
    def __init__(self, rect, color1=(150, 150, 150)):
        Region.__init__(self, *rect)

        self.text = font.render("X", False, (255, 255, 255))
        self.selected = False
        self.just_pressed = False

        self.body_color = color1
        self.border_color = (0,0,0)
    
    def is_over(self, state, pos):
        if self.rect.collidepoint(pos):
            if state[0] and not self.just_pressed:
                self.selected = not self.selected
                self.just_pressed = True
            elif not state[0]:
                self.just_pressed = False
            return True
        return False

    def draw(self):
        pygame.draw.rect(screen, self.border_color, self.border_rect)
        if self.selected:
            self.draw_text()
        pygame.draw.rect(screen, self.body_color, self.rect, width=5)
        
    def draw_text(self):
        x, y = self.rect.topleft
        screen.blit(self.text, (x+6,y-10))

    def update(self, state, pos):
        self.is_over(state, pos)
        self.draw()
                      
class FileManager(Region):
    def __init__(self, rect):
        Region.__init__(self, *rect)

        self.color1 = (150, 150, 150)
        self.color2 = (120, 120, 120)

        self.cwd = os.getcwd()
        self.get_files()

        self.selected = None

    def get_files(self, extension=".png"):
        self.files = [] # list of dictionaries

        txt_off = [10, 10]
        img_off = [300,5]
        spacing = [150, 70] #horizontal, vertical

        index = 0
        for file in os.listdir(self.cwd):
            if file.endswith(extension):
                self.files.append({"name":str(file), 
                                   "img":scale_image(pygame.image.load(file).convert_alpha(), width=100, height=50),
                                   "text":font.render(str(file), False, (255, 255, 255)),
                                   "rect":pygame.Rect(self.rect.x, self.rect.y+spacing[1]*index,self.rect.width-self.rect.x, 60),
                                   "rectcolor":self.color1,
                                   "imgpos": (self.rect.x+img_off[0]+spacing[0], self.rect.y+img_off[1]+spacing[1]*index),
                                   "textpos": (self.rect.x+txt_off[0], self.rect.y+txt_off[1]+spacing[1]*index),
                                   "checkbox":Checkbox((self.rect.x+img_off[0]+spacing[0]+110, self.rect.y+img_off[1]+spacing[1]*index+10,
                                                        30, 30))})
                
                scale_image(pygame.image.load(file).convert_alpha(), 100, 60)
                index += 1

    def display_files(self, state, pos):
        for file in self.files:
            pygame.draw.rect(screen, file["rectcolor"], file["rect"])
            screen.blit(file["text"], file["textpos"])
            screen.blit(file["img"], file["imgpos"])
            file["checkbox"].update(state, pos)

    def is_over(self, pos):
        for file in self.files:
            if file["rect"].collidepoint(pos):
                file["rectcolor"] = self.color2
            else:
                file["rectcolor"] = self.color1

    def get_selected_files(self):
        selected = [img["name"] for img in self.files if img["checkbox"].selected]
        return selected
    
    def update(self, state, pos):
        self.draw()
        self.is_over(pos)
        self.display_files(state, pos)

class Settings(Region):
    def __init__(self, rect, file_manager):
        Region.__init__(self, *rect)

        self.path = os.getcwd()

        self.title = font.render("Settings", False, (255, 255, 255))
        self.colorkey = small_font.render(f"Colorkey: {COLORKEY}", False, (255, 255, 255))
        self.confirm = font.render("Confirm?", False, (255, 255, 255))
        self.destination = font.render("Destination", False, (255, 255, 255))
        self.stitch = small_font.render("Stitch into One?", False, (255, 255, 255))
        self.save_path = small_font.render("", False, (255, 255, 255))

        #----- UI Elements -----#
        self.ui_elements = {"confirm": Button((self.rect.x+80, HEIGHT-75, 40, 40), "Y", 
                                              color1=(30,255,150), color2=(10,235,70), 
                                              on_click=kick_off_actual_functionality, parent=[file_manager, self]),
                            "destination": Button((self.rect.x+35, self.rect.y+400, 120, 40), "Browse", 
                                                  on_click=browseFiles, parent=self),
                            "stitch":Checkbox((self.rect.x+140, self.rect.y+100, 30, 30))}
        
    def draw_text(self):
        x, y = self.rect.topleft
        screen.blit(self.title, (x+35, y+10))
        screen.blit(self.confirm, (x+35, HEIGHT-125))
        screen.blit(self.destination, (x+25, y+330))
        screen.blit(self.save_path, (x+15, y+370))

    def update_path(self, path):
        self.path = path
        self.save_path = small_font.render(parse_path(self.path, 2), False, (255, 255, 255))

    def draw_colorkey(self):
        x, y = self.rect.topleft
        screen.blit(self.colorkey, (x+15, y+50))
        pygame.draw.rect(screen, COLORKEY, (x+160, y+50, 20, 20))

    def draw_stitch(self):
        x, y = self.rect.topleft
        screen.blit(self.stitch, (x+15, y+100))

    def update_ui(self, state, pos):
        for _, item in self.ui_elements.items():
            item.update(state, pos)

    def update(self, state, pos):
        self.draw()
        self.draw_text()
        self.draw_colorkey()
        self.draw_stitch()
        self.update_ui(state, pos)

class FolderBrowser(Region):
    def __init__(self, rect, file_manager):
        Region.__init__(self, *rect)

        self.file_manager = file_manager

        self.update_path()
        self.ui_elements = {"browse":Button((self.rect.x+440, self.rect.y+25, 120, 50), "Browse", on_click=browseFiles, parent=self)}

    def update_path(self, path=os.path.dirname(__file__.replace("\\","/"))):
        self.path = path
        self.title = small_font.render(f"CWD: {parse_path(self.path)}", False, (255, 255, 255))
        self.file_manager.cwd = path
        self.file_manager.get_files()

    def update_ui(self, state, pos):
        for _, item in self.ui_elements.items():
            item.update(state, pos)
            
    def draw_text(self):
        x, y = self.rect.topleft
        screen.blit(self.title, (x+10, y+20))

    def update(self, state, pos):
        self.draw()
        self.update_ui(state, pos)
        self.draw_text()

if __name__ == "__main__":
    font = pygame.font.Font('data/at01.ttf', 50) # fix relative import
    small_font = pygame.font.Font('data/at01.ttf', 25) # fix relative import

    os.chdir(os.path.dirname(__file__)) # change the directory to the current file location
    f = FileManager((0,100,WIDTH-200,HEIGHT-100))
    s = Settings((WIDTH-201, 0, 200, HEIGHT), f)
    fol = FolderBrowser((0,0, WIDTH-200,100), f)

    while True:
        screen.fill((0,0,0))
        clock.tick(60)

        pos = pygame.mouse.get_pos()
        state = pygame.mouse.get_pressed()

        f.update(state, pos)
        s.update(state, pos)
        fol.update(state, pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()