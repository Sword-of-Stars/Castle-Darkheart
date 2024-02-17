import pygame

from PIL import Image
from ..builder.autotiler import Autotiler

from ..builder.builder_functions import get_config, get_path_id, screen_to_chunk2
from ..misc.core_functions import screen_to_world, world_to_screen, get_images, prep_image

PATH_TO_SAVE = "maps"

# TODO: Clean up autotiler and export to an external configuration file for cleanliness

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
        self.show_trigger = True
        self.place_multiple = True
        self.can_scale = True # Bugged for now :%

        self.just_clicked = False

        self.load_database()

        self.autotiler = Autotiler()

    def set_regions(self):
        self.header = self.gui.pages['main'].regions[2] # Future-proof later
        self.world = self.gui.pages['main'].regions[0]
        #self.palette = self.gui.pages['main'].regions[4]

    def select(self, item):
        self.selected = item

        if item is not None:
            self.update_selected(self.selected.id)
        else:
            self.update_selected("None")

    def place_asset(self, pos):
        self.world.place_asset(pos, self.layer, self.selected, 
                               self.current_map, snap_to=self.snap_to)
        
    def remove_asset(self, pos):
        # In later versions, condense this code from place asset
        tile_pos, chunk_id = self.world.get_tile_coord(pos)
        self.world.remove_asset(tile_pos, self.layer, chunk_id, self.current_map)

    def get_selected_chunk(self, pos):
        tile_pos, chunk_id = self.world.get_tile_coord(pos)

        print(f"Current chunk: {chunk_id}")
        print(f"{tile_pos}")
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


        for _, region in self.gui.get_current_page().regions.items():
            if str(region) == "trigger":
                if region.visible:
                    region.handle_text(event)

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
                #if self.selected.group == "tile":
                self.selected.rect.topleft = world_to_screen((x*self.world.SIZE, y*self.world.SIZE), 
                                                                self.world.offset, scale=self.world.scale)
               #elif self.selected.group == "decor":
                    #self.selected.rect.topleft = world_to_screen((x*self.world.SIZE, y*self.world.SIZE), 
                                                              #self.world.offset, scale=self.world.scale)
            else:
                self.selected.rect.topleft = pos

            if state[0]:
                if not self.just_clicked or self.place_multiple:
                    self.just_clicked = True
                    if self.world.is_over:
                        if not self.autotile or not self.selected.autotilable: #band-aid soln for now
                            self.place_asset(pos)
                        elif self.autotile and self.selected.group == "tile":
                            self.handle_autotile(pos)
                            
                else:
                    self.just_clicked = False
        
            self.selected.update(screen)
        else:
            if state[2]:
                self.remove(pos)

    def handle_autotile(self, pos):

        tile_pos, chunk_id = self.world.get_tile_coord(pos)
        cardinal_neighbors, diagonal_neighbors = self.world.get_neighbors(tile_pos, chunk_id)

        self.place_asset(pos)

        self.autotiler.update(tile_pos, chunk_id, self, self.selected.id, self.selected.group)

        for chunk_, tile_pos_, _ in cardinal_neighbors:
            tile = self.world.get_at(tile_pos_, chunk_, self.layer, self.current_map)
            if tile != None:
                if tile["tile_ID"].split(";")[1] == self.selected.id.split(";")[1]: # check if in same spritesheet
                    self.autotiler.update(tile_pos_, chunk_, self, self.selected.id, self.selected.group)

        for chunk_, tile_pos_, _ in diagonal_neighbors:
            tile = self.world.get_at(tile_pos_, chunk_, self.layer, self.current_map)
            if tile != None:
                if tile["tile_ID"].split(";")[1] == self.selected.id.split(";")[1]: # check if in same spritesheet
                    self.autotiler.update(tile_pos_, chunk_, self, self.selected.id, self.selected.group)
        
    def remove_asset_autotile(self, pos):
        # In later versions, condense this code from place asset
        tile_pos, chunk_id = self.world.get_tile_coord(pos)
        tile_del = self.world.get_at(tile_pos, chunk_id, self.layer, self.current_map)

        if tile_del != None:

            id_ = tile_del["tile_ID"]
            group = tile_del["group"]

            self.world.remove_asset(tile_pos, self.layer, chunk_id, self.current_map)

            cardinal_neighbors, diagonal_neighbors = self.world.get_neighbors(tile_pos, chunk_id)

            for chunk_, tile_pos_, _ in cardinal_neighbors:
                tile = self.world.get_at(tile_pos_, chunk_, self.layer, self.current_map)
                if tile != None:
                    if tile["auto?"]:
                        self.autotiler.update(tile_pos_, chunk_, self, id_, group)

            for chunk_, tile_pos_, _ in diagonal_neighbors:
                tile = self.world.get_at(tile_pos_, chunk_, self.layer, self.current_map)
                if tile != None:
                    if tile["auto?"]:
                        self.autotiler.update(tile_pos_, chunk_, self, id_, group)

    def remove(self, pos):
       # In later versions, condense this code from place asset
        tile_pos, chunk_id = self.world.get_tile_coord(pos)
        tile_del = self.world.get_at(tile_pos, chunk_id, self.layer, self.current_map)

        if tile_del != None:

            id_ = tile_del["tile_ID"]
            group = tile_del["group"]

            self.world.remove_asset(tile_pos, self.layer, chunk_id, self.current_map)

            if tile_del["auto?"]:

                cardinal_neighbors, diagonal_neighbors = self.world.get_neighbors(tile_pos, chunk_id)

                for chunk_, tile_pos_, _ in cardinal_neighbors:
                    tile = self.world.get_at(tile_pos_, chunk_, self.layer, self.current_map)
                    if tile != None:
                        if tile["auto?"]:
                            self.autotiler.update(tile_pos_, chunk_, self, id_, group)

                for chunk_, tile_pos_, _ in diagonal_neighbors:
                    tile = self.world.get_at(tile_pos_, chunk_, self.layer, self.current_map)
                    if tile != None:
                        if tile["auto?"]:
                            self.autotiler.update(tile_pos_, chunk_, self, id_, group)

class BuilderUI():
    def __init__(self, builder):
        self.builder = builder

        self.buttons = []

    def add_button(self):
        pass
