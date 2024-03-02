import pygame

from scripts.rendering.camera import screen_to_chunk

class Minimap():
    # pass to ui layer
    def __init__(self, camera):
        self.layer = 1

        self.rect =  pygame.rect.Rect(40,600,150,150)
        self.color = (30,30,30)

        self.visible_range = (500, 500)
        self.visible_tl = [camera.x - self.visible_range[0], camera.y - self.visible_range[1]]
        self.visible_br = [camera.x + self.visible_range[0], camera.y + self.visible_range[1]]


        self.mapfile = None

    def set_map(self, mapfile):
        self.mapfile = mapfile

    def move(self, camera):
        self.visible_tl = [camera.x - self.visible_range[0], camera.y - self.visible_range[1]]
        self.visible_br = [camera.x + self.visible_range[0], camera.y + self.visible_range[1]]

    def draw(self, camera, visible_chunks):

        ax, ay = screen_to_chunk((camera.x+camera.width//2, 
                                        camera.y+camera.height//2),
                                       (camera.x, camera.y))

        for chunk in visible_chunks:
            if chunk in self.mapfile:
                for tile in self.mapfile[chunk]:
                    if tile["tile_ID"] == "ss;1;0":
                        for overhang in self.mapfile[chunk]:
                            if "ss;0" in overhang["tile_ID"] and overhang["z-order"] == 1 and overhang["pos"] == tile["pos"]:
                                break
                        else:
                            size = 8
                            print(tile['pos'])
                            cx, cy = [int(x) for x in chunk.split(";")]
                            dx = (ax-cx)*4*size
                            dy = (ay-cy)*4*size
                            c = self.rect.center

                            x = c[0]+dx+tile['pos'][0]*size
                            y = c[1]+dy+tile['pos'][1]*size

                            pygame.draw.rect(camera.ui_surf, (255,0,0), (x,y, size, size))

    def get_visible_chunks(self, camera):
       
        ax, ay = screen_to_chunk(self.visible_tl, (camera.x, camera.y))
        bx, by = screen_to_chunk(self.visible_br, (camera.x, camera.y))

        c_dx = bx-ax+1 # +1 adds a bit of buffer for seamless drawing
        c_dy = by-ay+1
        
        chunk_map = []
    
        for x in range(-1, c_dx):
            for y in range(-1, c_dy):
                chunk_map.append(f"{ax+x};{ay+y}")
                    
        return chunk_map
    
   
    def update(self, camera):
        self.move(camera)
        pygame.draw.rect(camera.ui_surf, self.color, self.rect)

        c = self.get_visible_chunks(camera)
        self.draw(camera, c)


        #print(self.get_visible_chunks(camera))
        #camera.ui_surf.blit()