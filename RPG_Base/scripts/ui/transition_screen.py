import pygame, sys

class TransitionScreen():
    def __init__(self, screen, clock, camera):
        self.msg = '''
        Where are the brave men? All gone away
          Who in the land has courage to stay?
          Soldiers guard with spear and sword,
           Cannot stem the Mad King's horde
        '''

        self.author = '''
        - Vigil for Dragonkeep
           Age of Lament'''
        
    
        self.continue_msg = "Press any key to continue"

        self.font_lg = pygame.font.Font("data/fonts/oldenglish.ttf", 40)
        self.font_sm = pygame.font.Font("data/fonts/CloisterBlack.ttf", 52)

        self.msg_text = self.font_sm.render(self.msg, False, (255,255,255))
        center = (screen.get_size()[0]//2-100, screen.get_size()[1]//2-50)
        self.rect = self.msg_text.get_rect(center=center)
        self.msg_text.set_alpha(0)

        self.by_text = self.font_lg.render(self.author, False, (255,255,255))
        self.by_pos = (center[0]+100, center[1]+120)
        self.by_text.set_alpha(0)

        self.cont_text = self.font_lg.render(self.continue_msg, False, (255,255,255))
        self.cont_pos = (center[0]-100, center[1]+420)
        self.cont_text.set_alpha(0)


        self.screen = screen
        self.clock = clock
        self.camera = camera

        self.t = 0
        self.t_speed = 0.5

        self.fade_out = False
        self.black = pygame.surface.Surface(camera.display.get_size())
        self.black.fill((0,0,0))
        self.black.set_alpha(0)
        self.fade_alpha = 0
        self.fade_out_done = False

        self.wait = True

    def do_fade(self):
        self.fade_alpha = min(255, self.fade_alpha+2)
        self.black.set_alpha(self.fade_alpha)

        if self.fade_alpha >=254:
            self.fade_out_done = True

        pygame.mixer.music.fadeout(6400)

    def reset(self):
        self.t = 0
        self.fade_alpha = 0
        self.fade_out = False
        self.fade_out_done = False
        self.wait = False

        self.by_text.set_alpha(0)
        self.cont_text.set_alpha(0)

        self.black = pygame.surface.Surface(self.camera.display.get_size())
        self.black.fill((0,0,0))
        self.black.set_alpha(0)

        self.t_speed = 1

        pygame.mixer.music.stop()
        pygame.mixer.music.load("data/music/main-1/main-3.mp3")
        pygame.mixer.music.play(-1)


    def update(self):
        if self.t < 600:
            self.t += self.t_speed
        
        if self.t > 50:
            self.msg_text.set_alpha(min(self.t-50, 255))
        if self.t > 100:
            self.by_text.set_alpha(min(self.t-100, 255))
        if self.t > 300:
            self.t_speed = 3
            self.cont_text.set_alpha(min(self.t-300, 255))


        self.camera.display.blit(self.msg_text, self.rect)
        self.camera.display.blit(self.by_text, self.by_pos)
        self.camera.display.blit(self.cont_text, self.cont_pos)

    def run(self):
        self.camera.fill()
        self.clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                
                elif self.t >= 300 or not self.wait:
                    self.fade_out = True

        if self.fade_out:
            self.do_fade()

        self.update()
        self.camera.display.blit(self.black, (0,0))

        self.camera.draw_world()
        self.camera.update()

        if self.fade_out_done:
            self.by_text.set_alpha(0)
            self.cont_text.set_alpha(0)
            self.black.set_alpha(0)
            self.t = 0
            return "game"
        return "transition"