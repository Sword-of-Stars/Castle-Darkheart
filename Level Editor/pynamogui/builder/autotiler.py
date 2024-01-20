import pygame, sys

class Autotiler:
    def __init__(self, world, config_path):
        self.world = world

    def autotile(self, tiles):
        # Where 'tiles' is a dictionary of the form {"3;1":[tiles]}
        for key, item in tiles.items():
            for tile in item:
                tile["val"] = 0
                neighbors = self.world.get_neigbors(tile["pos"], key)
                # neighbors is a list of lists, with the first term 
                # being a chunk, the second a tile pos

                # A bit of bad design, I know, but this outputs in the 
                # order u,r,d,l
                # up is 1, right=2, down=4, left=8
                for i, n in enumerate(neighbors):
                    if n[1] in tiles[n[0]]:
                        tile["val"] += 2**(i)