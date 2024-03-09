import pygame 

class Button():
    def __init__(self, img, pos, scale=1, glow="data/menu_images/glow.png", hover_sound=None, selected_sound=None):
        self.img = pygame.image.load(img)
        self.img = pygame.transform.scale_by(self.img, scale).convert_alpha()
        self.rect = self.img.get_rect(x=pos[0], y=pos[1])

        self.glow = pygame.image.load("data/menu_images/glow.png")
        self.glow = pygame.transform.scale_by(self.glow, scale).convert_alpha()
        self.glow_offset = (-40,-40)

        self.hover_sound = hover_sound
        if self.hover_sound != None:
            self.hover_sound = pygame.mixer.Sound(hover_sound)

        self.selected_sound = selected_sound
        if self.selected_sound != None:
            self.selected_sound = pygame.mixer.Sound(selected_sound)

        self.over = False
        self.selected = False

    def is_over(self, pos):
        state = pygame.mouse.get_pressed()[0]
        if self.rect.collidepoint(pos):
            if not self.over:
                self.hover_sound.play()
            self.over = True

            if state and not self.selected:
                self.selected = True
                if self.selected_sound != None:
                    self.selected_sound.play()
        else:
            self.over = False


    def update(self, screen, pos):
        self.is_over(pos)
        if self.over:
            pos = self.rect.topleft
            screen.blit(self.glow, (pos[0]+self.glow_offset[0], 
                                    pos[1]+self.glow_offset[1]))

        screen.blit(self.img, self.rect)
