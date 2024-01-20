import pygame
import json

from scripts.entities.obstacle import ObstacleImage
from scripts.utils.core_functions import load_json, world_to_screen

class Map:
    def __init__(self, mapfile, db, camera):
        self.db = db # tile database for easy reference
        self.loaded_chunks = None
        self.obstacles = []
        self.map_dict = {}
        self.config = load_json("maps/config")

        self.pixel_size = 4 # One pixel takes a 4x4 region on screen
        self.chunk_size = 64

        self.load_map(mapfile, camera)

    def load_map(self, mapfile, camera):
        chunks = load_json(mapfile)["chunks"]

        for key, chunk in chunks.items(): # Set to visible later, rough for now
            cx, cy = [int(x) for x in key.split(";")]
            
            self.map_dict[key] = []
            for tile in chunk:
                if tile['group'] == 'tile':
                    x, y = tile['pos']
                    
                    img = pygame.transform.scale_by(self.db.get_tile_image(tile['tile_ID']), (camera.scale))

                    pos = world_to_screen(((x+cx*self.pixel_size)*self.chunk_size, 
                                           (y+cy*self.pixel_size)*self.chunk_size), 
                                           (camera.x, camera.y), (camera.scale))

                    self.map_dict[key].append(ObstacleImage(*pos, img, tile["z-order"]))

    def draw_world(self, camera):
        self.obstacles = [] # Later, update less frequently
        visible_chunks = camera.get_visible_chunks()

        for chunk in visible_chunks: # Set to visible later, rough for now
            if chunk in self.map_dict:
                for tile in self.map_dict[chunk]:
                    self.obstacles.append(tile)

        for tile in self.obstacles:
            camera.to_render(tile)
        #return self.obstacles