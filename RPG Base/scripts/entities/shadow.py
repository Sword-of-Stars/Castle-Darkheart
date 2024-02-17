import pygame

def circle_surf(rect, color):
    surf = pygame.Surface((rect.width, rect.height))
    pygame.draw.ellipse(surf, color, rect)
    surf.set_colorkey((0, 0, 0))
    return surf

class Shadow():
    def __init__(self, rect, layer):
        self.rect = pygame.rect.Rect(rect)
        self.layer = layer

        self.surf = circle_surf(self.rect, (59,59,59))
    
    def set_pos(self, pos):
        self.pos = pos

    def draw(self, camera):
        camera.display.blit(self.surf, self.pos, special_flags=pygame.BLEND_RGB_SUB)

    def update(self, pos, camera):
        self.set_pos(pos)
        camera.to_render(self)