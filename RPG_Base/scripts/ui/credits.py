import pygame,sys

msgs = '''
Where are the brave men? All gone away
Who in the land has courage to stay?
Soldiers guard with spear and sword,
Cannot stem the Mad King's horde

Gone are the brave men, none here to stay
Oh, had we found an enlightened way
Wand'ring with no path to find
Gone are now both will and mind

Where are the brave men? Lost in the fray
Minds muddled o'er, now chaos obey
Shattering stars, the moon bleeds red
Out to the night hath now reason fled

Dead are the brave men, for them we pray
Stilled are their blades, now quiet they lay
Slain were they by shade and sword
Sent to join their mighty Lord

Yet Death holds but a passing sway,
Joy will come upon His day

Made by Matthew Wanta
Special thanks to JV, B2, '26 for his amazing cover art

Thanks for playing!
'''


class Credits():
    def __init__(self, width, height, camera, clock, mouse, screen):

        self.width = width
        self.height = height

        fade_out = pygame.surface.Surface((width, height))
        fade_out.fill((0,0,0))
        fade_out.set_alpha(0)
        self.fade_out = fade_out
        self.fade_t = 0

        self.font_lg = pygame.font.Font("data/fonts/oldenglish.ttf", 52)
        self.font_sm = pygame.font.Font("data/fonts/CloisterBlack.ttf", 40)

        self.title = "Vigil for Dragonkeep"
        self.title_render = self.font_lg.render(self.title, False, (240,240,240))

        self.hymn = self.font_sm.render(msgs, False, (240,240,240))
    
        self.camera = camera
        self.clock = clock
        self.mouse = mouse
        self.screen = screen

        camera.vignette = 0.9

        self.pos = height

        self.speed = 1

    def start(self):
        pygame.mixer.music.load('data/music/main-1/main-3.mp3')
        pygame.mixer.music.play(-1)

        self.camera.fill()
    
          
    def update(self):
        self.pos -= self.speed
        self.camera.display.blit(self.title_render, (700,self.pos))
        self.camera.display.blit(self.hymn, (600,self.pos+100))
      
    def run(self):
        self.camera.fill()
        self.clock.tick(60)

        pygame.display.set_caption((str(self.clock.get_fps())))

        pos = pygame.mouse.get_pos()
    

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        self.update()

        self.camera.draw_world()
        self.camera.update()

