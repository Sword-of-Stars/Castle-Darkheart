import pygame

FONT_PATH = "data/fonts/oldenglish.ttf"
font = pygame.font.Font(FONT_PATH, 52)
font_sm = pygame.font.Font(FONT_PATH, 32)


class Tutorial():
    def __init__(self, camera, active=False):
        self.active = active

        self.color = (240,240,240)
        
        msgs = ["WASD to move","Press space while moving to dash","Left click to attack","Right click to heal","Complete the hymn to open the door. Good luck!"]
        self.msgs = []
        for msg in msgs:
            self.msgs.append(font.render(msg, True, self.color))
        self.msg = 0

        self.pos = (camera.width//2, 150)

        self.timer_max = 40
        self.timer = self.timer_max

        self.fade_timer = 0

        self.continue_msg = font_sm.render("Press X to continue", True, self.color)

    def next(self):
        if self.msg +1 < len(self.msgs):
            if self.timer <= 0:
                self.msg += 1
                self.timer = self.timer_max

        else:
            self.active = False

    def update(self, camera):
        if self.active:
            width, height = self.msgs[self.msg].get_size()
            pos = (camera.width//2-width//2, 150)

            width2, height = self.continue_msg.get_size()
            pos2 = (camera.width//2-width2//2, 215)
            
            camera.ui_surf.blit(self.msgs[self.msg], pos)
            camera.ui_surf.blit(self.continue_msg, pos2)

            

            if self.timer > 0:
                self.timer -= 1
        