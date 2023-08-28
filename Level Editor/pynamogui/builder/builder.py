import pygame

from PIL import Image

from ..builder.builder_functions import get_config, get_path_id, screen_to_chunk2
from ..misc.core_functions import screen_to_world, world_to_screen, get_images, prep_image

PATH_TO_SAVE = "maps"

get_config(PATH_TO_SAVE)

class Builder():
    def __init__(self, gui):
        self.selected = None
        self.layer = 0
        self.z_order = 0

        self.database = {}
        self.current_map = {"name":"The Golden Plains", "chunks":{"0;0":[]}} # Save maps to this location/file
        self.current_map_path = "maps"

        self.gui = gui

        self.path_to_save = PATH_TO_SAVE

        # Modes and Pseudofeatures #
        self.snap_to = True
        self.autotile = True
        self.show_grid = True
        self.place_multiple = True
        self.can_scale = True # Bugged for now :%

        self.just_clicked = False

        self.load_database()


    def set_regions(self):
        self.header = self.gui.pages['main'].regions[2] # Future-proof later
        self.world = self.gui.pages['main'].regions[0]
        self.palette = self.gui.pages['main'].regions[4]

    def select(self, item):
        self.selected = item

        if item is not None:
            self.update_selected(self.selected.id)
        else:
            self.update_selected("None")

    def place_asset(self, pos):
        # Not the cleanest way, but this is how I've been doing garbage collection for a while, so it's good enough. 
        # Additionally, I should update these screen-to-world functions to better accomodate pixel size. 
        
        cx, cy = screen_to_chunk2(pos, self.world.offset, self.world.scale)
        px, py = self.world.get_grid_coord(pos)

        py = int(-1-py-4*cy)
        if py < 0:
            py = 0


        # Create and place new object reference - doesn't need to be over-optimized
        new_obj = {"tile_ID":self.selected.id, "group":self.selected.group,
                    "z-order":self.layer,"pos":[int(px-4*cx), py]}
        
        #if int(-1-py-4*cy) < 0:
            #print("OH, ****")

        
        chunk_id = f"{cx};{cy}"
        if chunk_id not in self.current_map['chunks']:
            self.current_map['chunks'][chunk_id] = []

        for i in self.current_map['chunks'][chunk_id]:
            if i["pos"] == new_obj['pos'] and i['z-order'] == new_obj['z-order']:
                self.current_map['chunks'][chunk_id].remove(i)
                break           

        self.current_map['chunks'][chunk_id].append(new_obj)

        #print(self.current_map)
        
    def remove_asset(self, pos):
        # In later versions, condense this code from place asset
        cx, cy = screen_to_chunk2(pos, self.world.offset, scale=self.world.scale)
        px, py = self.world.get_grid_coord(pos)
        obj_pos = [int(px-4*cx), int(-1-py-4*cy)]
        chunk_id = f"{cx};{cy}"

        if chunk_id not in self.current_map['chunks']:
            self.current_map['chunks'][chunk_id] = []

        for i in self.current_map['chunks'][chunk_id]:
            if i["pos"] == obj_pos and i['z-order'] == self.layer:
                self.current_map['chunks'][chunk_id].remove(i)
                break

    def get_selected_chunk(self, pos):
        cx, cy = screen_to_chunk2(pos, self.world.offset, scale=self.world.scale)
        px, py = self.world.get_grid_coord(pos)
        obj_pos = [int(px-4*cx), int(-1-py-4*cy)]
        chunk_id = f"{cx};{cy}"

        print(f"Current chunk: {chunk_id}")
        print(f"{obj_pos}")
        if chunk_id not in self.current_map['chunks']:
            self.current_map['chunks'][chunk_id] = []
        print(f"Chunk Data: {self.current_map['chunks'][chunk_id]}")

    def load_database(self):
        self.config = get_config(self.path_to_save)
        for key, item in self.config.items():
            with Image.open(item) as img:
               images = get_images(img)
            for index, image in enumerate(images):
                _id = f"ss;{key};{index}" # Currently, ss stands for spritesheet, may be deprecated later on
                image = prep_image(image, 4) # Magic number
                self.add_to_db(_id, image)

    def add_to_db(self, _id, img):
        self.database[_id] = img

    def load_map(self, path): # Not certain how this fits together, but OK
        pass

    def save_map(self):
        pass

    def handle_button(self, event):
        if event.key == pygame.K_UP:
            self.layer += 1
            self.layer = min(10, self.layer) # Maximum layer is 10
            self.update_layer()

        elif event.key == pygame.K_DOWN:
            self.layer -= 1
            self.layer = max(-10, self.layer) # Minimum layer is -10
            self.update_layer()

    def update_layer(self):
        self.header.modify_text('layer_num', self.layer)

    def update_selected(self, txt):
        self.header.modify_text('selected_txt', txt)

    def update(self, pos, state, screen):
        if self.selected != None:
            self.selected.scale(self.world.scale)
            x, y = self.world.get_grid_coord(pos)

            if self.snap_to:
                # Not sure if I want the sprite to snap to the center, or topleft
                # Regardless, each sprite will likely need a config setup to establish offsets
                if self.selected.group == "tile" or self.selected.group == "decor":
                    self.selected.rect.bottomleft = world_to_screen((x*self.world.SIZE, -y*self.world.SIZE), 
                                                                self.world.offset, scale=self.world.scale)
                #elif self.selected.group == "decor":
                   # self.selected.rect. = world_to_screen((x*self.world.SIZE, -y*self.world.SIZE), 
                                                              #  self.world.offset, scale=self.world.scale)
            else:
                self.selected.rect.center = pos

            if state[0]:
                if not self.just_clicked or self.place_multiple:
                    self.just_clicked = True
                    if self.world.is_over:
                        self.place_asset(pos)
            else:
                self.just_clicked = False
        
            self.selected.update(screen)
        else:
            if state[2]:  
                self.remove_asset(pos)

class BuilderUI():
    def __init__(self, builder):
        self.builder = builder

        self.buttons = []

    def add_button(self):
        pass
