import pygame, math
from scripts.utils.core_functions import get_images, prep_image

def mana_surf(rect):
    surf = pygame.Surface((rect.width, rect.height))
    surf.set_colorkey((0, 0, 0))
    return surf

class HUD():
    def __init__(self, player, camera):
        self.surf = camera.ui_surf

        self.player = player
        player.set_HUD(self)

        self.images = get_images("data/ui.png")

        self.heart = prep_image(self.images[0], 4, colorkey=(255,255,255)).convert_alpha()
        self.white_heart = pygame.mask.from_surface(self.heart).to_surface().convert_alpha()
        self.white_heart.set_colorkey((0,0,0))
        self.heart_spacing = self.heart.get_rect().width + 10
        self.heart_offset = [20,20]

        self.zeal = pygame.transform.rotate(prep_image(self.images[1], 6, colorkey=(255,255,255)), 270)
        self.zeal_offset = [20,65]

        self.flash_timer_MAX = 6
        self.flash_timer = self.flash_timer_MAX # number of frames hearts turn white
        self.damage_taken = 0


    def flash(self, damage=1):
        self.flash_timer = self.flash_timer_MAX
        self.damage_taken = damage

    def draw_health(self):
        if self.flash_timer > 0:
            self.flash_timer -= 1

            i, j = 0,0

            for i in range(max(0,self.player.health)):
                pos = (self.heart_offset[0] + self.heart_spacing*i, self.heart_offset[1])
                self.surf.blit(self.heart, pos)

            for j in range(self.player.health, self.player.health + self.damage_taken):
                pos = (self.heart_offset[0] + self.heart_spacing*(j), self.heart_offset[1])
                self.surf.blit(self.white_heart, pos)
        else:
            for i in range(self.player.health):
                pos = (self.heart_offset[0] + self.heart_spacing*i, self.heart_offset[1])
                self.surf.blit(self.heart, pos)

    def draw_zeal(self):
        self.surf.blit(self.zeal, self.zeal_offset)

    def update(self):
        self.surf.fill(pygame.Color(0,0,0,0))

        self.draw_health()
        self.draw_zeal()
       
        
