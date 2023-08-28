import pygame, sys

from ..gui_elements.regions import WorldBox, ScrollBox, TextBox, ImageBox, BlankRegion
from ..gui_elements.elements import ImgButton_base, Checkbox
from ..builder import Builder
from ..misc.core_functions import load_json, get_mouse_info

class GUI:
    def __init__(self):
        self.pages = {}
        self.current_page = None
        self.builder = Builder(self)

    def init_builder(self):
        self.builder.set_regions()

    def load(self):
        pass

    def set_screen(self, screen):
        self.screen = screen

    def add_page(self, page):
        self.pages[page.name] = page

    def remove_page(self, page):
        if page.name in self.pages:
            pass # Remove it, forgot exact syntax

    def handle_scroll(self, event):
        pos = get_mouse_info()[2]
        if self.current_page != None:
            self.pages[self.current_page].handle_scroll(event, pos)

    def handle_button(self, event):
        self.builder.handle_button(event)

    def update(self):
        rel, state, pos = get_mouse_info()
        if self.current_page != None: # Maybe make a default page
            self.pages[self.current_page].update(pos, state, rel, self.screen)

    def exit(self):
        print("Saving files. Please be patient.")
        pygame.quit()
        sys.exit()

class Page():
    def __init__(self, config_path):
        self.config_path = config_path

        self.regions = {}
        self.load()

        self.gui = gui
        self.gui.add_page(self)

    def load(self):
        self.config = load_json(self.config_path)
        self.name = self.config['name']
        for region in self.config['regions']:
            if region['type'] == 'blank':
                self.regions[region["ID"]] = BlankRegion(region) 
            elif region['type'] == 'text':
                self.regions[region["ID"]] = TextBox(region, gui) 
            elif region['type'] == 'world':
                self.regions[region["ID"]] = WorldBox(region, gui.builder)
            elif region['type'] == 'image':
                self.regions[region["ID"]] = ImageBox(region, gui.builder)
            elif region['type'] == 'scroll':
                self.regions[region["ID"]] = ScrollBox(region, gui)
            elif region['type'] == 'button':
                self.regions[region["ID"]] = ImgButton_base(region, gui)
            elif region['type'] == 'checkbox':
                self.regions[region["ID"]] = Checkbox(region, gui)
            else:
                print(f"'{region['type']}' is not a valid region type.")
        self.regions = dict(sorted(self.regions.items()))

    def handle_scroll(self, event, pos):
        for _, region in self.regions.items():
            region.scroll_event(event, pos)

    def update(self, pos, state, rel, screen):
        for _, region in self.regions.items():
            region.update(pos, state, rel, screen)
        gui.builder.update(pos, state, screen)
    
gui = GUI()
