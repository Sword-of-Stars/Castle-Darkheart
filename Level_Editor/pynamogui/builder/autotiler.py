import pygame, sys

class Autotiler:
    def __init__(self):
        self.cardinal = {
                "up": 1,
                "right": 2,
                "down": 4,
                "left": 8
                }
            
        self.diagonal = {
            "up-left": 16,
            "up-right": 32,
            "down-left": 64,
            "down-right": 128,
            }

        self.autotile_conversion = {4:0,5:1,1:2,0:3,6:4,7:5,3:6,2:7,
            14:8,15:9,11:10,10:11,12:12,13:13,9:14,8:15,
            31:16,135:17,39:18,79:19,142:20,239:21,191:22,43:23,78:24,
            223:25,127:26,27:27,47:28,77:29,29:30,143:31,134:32,
            167:33,175:34,35:35,207:36,111:37,255:38,59:39,206:40,999:41,159:42,63:43,
            76:44,95:45,93:46,25:47,256:48}

        self.offsets = {10:-2, 11:-2, 14:-2, 15:-2, 23:-2, 27:-2, 39:-2, 47:-2}

    def update(self, tile_pos, chunk, builder, id, group):
        cardinal_neighbors, diagonal_neighbors = builder.world.get_neighbors(tile_pos, chunk)

        bitmap_sum = 0

        for chunk_, tile_pos_, direction in cardinal_neighbors:
            tile = builder.world.get_at(tile_pos_, chunk_, builder.layer, builder.current_map)
            if tile != None:
                if tile["tile_ID"].split(";")[1] == id.split(";")[1]:
                    bitmap_sum += self.cardinal[direction]
                else:
                    for diag_tile in reversed(diagonal_neighbors):
                        if direction in diag_tile[2]:
                            diagonal_neighbors.remove(diag_tile)
            else:
                for diag_tile in reversed(diagonal_neighbors):
                    if direction in diag_tile[2]:
                        diagonal_neighbors.remove(diag_tile)

        for chunk_, tile_pos_, direction in diagonal_neighbors:
            tile = builder.world.get_at(tile_pos_, chunk_, builder.layer, builder.current_map)
            if tile != None:
                if tile["tile_ID"].split(";")[1] == id.split(";")[1]:
                    bitmap_sum += self.diagonal[direction]

        tile_index = self.autotile_conversion[bitmap_sum]
        spritesheet, index, _ = id.split(";")

        #self.selected.img = self.database[f"{spritesheet};{index};{self.layer+10}"]

        offset = 0
        if tile_index in self.offsets:
            offset = self.offsets[tile_index]

        #print(bitmap_sum)
        builder.world.place_asset_by_coord(chunk, tile_pos, builder.layer, group, 
                                        f"{spritesheet};{index};{tile_index}", builder.current_map, offset=[offset,0], auto=True)

        return tile_index