import pygame, sys

class MenuScreen():
    def __init__(self):
        self.castle = pygame.image.load("data/menu_images/castle.png")
        self.castle = pygame.transform.scale(self.castle, (width, height)).convert_alpha()

        self.clouds = pygame.image.load("data/menu_images/clouds.png").convert_alpha()
        self.clouds = pygame.transform.scale(self.clouds, (width, height)).convert_alpha()

        self.fg_01 = pygame.image.load("data/menu_images/foreground_1.png").convert_alpha()
        self.fg_01 = pygame.transform.scale(self.fg_01, (width, height)).convert_alpha()
       
        self.fg_02 = pygame.image.load("data/menu_images/foreground_2.png").convert_alpha()
        self.fg_02 = pygame.transform.scale(self.fg_02, (width, height)).convert_alpha()

        self.fg_03 = pygame.image.load("data/menu_images/foreground_3.png").convert_alpha()
        self.fg_03 = pygame.transform.scale(self.fg_03, (width, height)).convert_alpha()

        self.sky = pygame.image.load("data/menu_images/sky.png").convert_alpha()
        self.sky = pygame.transform.scale(self.sky, (width, height)).convert_alpha()
        
        self.title = pygame.image.load("data/menu_images/title.png").convert_alpha()
        self.title = pygame.transform.scale(self.title, (width, height)).convert_alpha()

        self.castle.set_colorkey((255,255,255))
        self.clouds.set_colorkey((255,255,255))
        self.fg_01.set_colorkey((255,255,255))
        self.fg_02.set_colorkey((255,255,255))
        self.fg_03.set_colorkey((255,255,255))
        self.sky.set_colorkey((255,255,255))
        self.title.set_colorkey((255,255,255))

    def update(self, screen):
        screen.blit(self.sky, (0,0))
        screen.blit(self.castle, (0,0))
        screen.blit(self.fg_03, (0,0))
        screen.blit(self.fg_02, (0,0))
        screen.blit(self.fg_01, (0,0))
        screen.blit(self.clouds, (0,0))
        screen.blit(self.title, (0,0))




clock = pygame.time.Clock()
width, height = 1200,800
screen = pygame.display.set_mode((width,height))

menu = MenuScreen()

menu.update(screen)
pygame.image.save(screen, "data/menu_images/composite_menu.png")


while True:
    screen.fill((0,0,0))
    clock.tick(60)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    menu.update(screen)

    pygame.display.flip()