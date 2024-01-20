import pygame, sys

from scripts.utils.core_functions import load_json, get_images, prep_image

class Database():
    def __init__(self):
        self.config = load_json("maps/config")
        self.db = {}
        self.load_images()

    def load_images(self):
        for key, item in self.config.items():
            images = [prep_image(x, 4) for x in get_images(item)]
            self.db[key] = images

    def get_tile_image(self, tile_id):
        sheet, index = tile_id.split(";")[1:]

        return self.db[sheet][int(index)]
