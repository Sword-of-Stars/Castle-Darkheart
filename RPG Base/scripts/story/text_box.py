import pygame, sys

from scripts.utils.core_functions import prep_image

font_lg = pygame.font.Font("data/fonts/oldenglish.ttf", 40)
font_small = pygame.font.Font("data/fonts/oldenglish.ttf", 32)


class TextBox():
    def __init__(self, character, msg):
        self.pos = [235,575] # read from config, need to make a centralized config file

        self.character = character
        self.character_text = font_lg.render(character, False, (255,255,255))
        self.text_pos = [400,600]
        self.overlay = prep_image(pygame.image.load("data/portrait_overlay.png"), 3, colorkey=(0,0,0))

        self.msg = msg

    def update(self, camera):
        camera.ui_surf.blit(self.character_text, self.text_pos)
        camera.ui_surf.blit(self.overlay, self.pos)

    