import pygame, sys

#from scripts.ui.button import Button

pygame.init()

class Button():
    def __init__(self, img, pos, scale=1, hover_sound=None):
        self.img = pygame.image.load(img)
        self.img = pygame.transform.scale_by(self.img, scale).convert_alpha()
        self.rect = self.img.get_rect(x=pos[0], y=pos[1])

        self.glow = pygame.image.load("data/menu_images/glow.png")
        self.glow = pygame.transform.scale_by(self.glow, scale).convert_alpha()
        self.glow_offset = (-40,-40)

        self.hover_sound = hover_sound
        if self.hover_sound != None:
            self.hover_sound = pygame.mixer.Sound(hover_sound)

        self.over = False
        self.selected = False

    def is_over(self, pos):
        if self.rect.collidepoint(pos):
            if not self.over:
                self.hover_sound.play()
            self.over = True
        else:
            self.over = False


    def update(self, screen, pos):
        self.is_over(pos)
        if self.over:
            pos = self.rect.topleft
            screen.blit(self.glow, (pos[0]+self.glow_offset[0], 
                                    pos[1]+self.glow_offset[1]))

        screen.blit(self.img, self.rect)

class MenuScreen():
    def __init__(self):
        
        self.images = {
            "castle": {
                "image": pygame.image.load("data/menu_images/castle.png"),
                "parallax": 0.0,
                "layer": 0,
                "pos": [0,0]
            },
            "clouds_1": {
                "image": pygame.image.load("data/menu_images/clouds.png"),
                "parallax": 1.0,
                "layer": 0,
                "pos": [0,0]
            },
            "clouds_2": {
                "image": pygame.image.load("data/menu_images/clouds.png"),
                "parallax": 1.0,
                "layer": 0,
                "pos": [0,0]
            },
            "fg_01": {
                "image": pygame.image.load("data/menu_images/foreground_1.png"),
                "parallax": 2,
                "layer": 3,
                "pos": [0,0]
            },
            "fg_02": {
                "image": pygame.image.load("data/menu_images/foreground_2.png"),
                "parallax": 0.7,
                "layer": 1,
                "pos": [0,0]
            },
            "fg_03": {
                "image": pygame.image.load("data/menu_images/foreground_3.png"),
                "parallax": 1.0,
                "layer": 2,
                "pos": [0,0]
            },
            "sky": {
                "image": pygame.image.load("data/menu_images/sky.png"),
                "parallax": 0.0,
                "layer": -1,
                "pos": [0,0]
            },
            "title": {
                "image": pygame.image.load("data/menu_images/title.png"),
                "parallax": 0.0,
                "layer": 4,
                "pos": [10,10]
            }
        }

        self.cloud_speed = 1
        self.dist = 50

        self.play_button = Button("data/menu_images/start.png", (60,250), scale=0.75, hover_sound="data/sound_effects/heartbeat_hover.wav")
        self.settings_button = Button("data/menu_images/settings.png", (60,425), scale=0.75, hover_sound="data/sound_effects/heartbeat_hover.wav")


        self.load_images()
    
    def load_images(self):
        for image_name, image_data in self.images.items():
            if image_name == "title":
                image_data["image"] = pygame.transform.scale_by(image_data["image"], 0.5).convert_alpha()
            elif image_name == "sky" or image_name == "castle":
                image_data["image"] = pygame.transform.scale(image_data["image"], (width, height)).convert_alpha()
            else:
                img_width, _ = image_data["image"].get_size()
                factor = (width+self.dist)/img_width
                image_data["image"] = pygame.transform.scale_by(image_data["image"], factor).convert_alpha()
                img_width, img_height = image_data["image"].get_size()

                if image_name == "clouds_1":
                    image_data["pos"] = [0, 0]
                elif image_name == "clouds_2":
                    image_data["image"] = pygame.transform.flip(image_data["image"], True, False).convert_alpha()
                    image_data["pos"] = [img_width, 0]
                else:
                    image_data["pos"] = [-self.dist//2, height-img_height]
            
            image_data["original_pos"] = image_data["pos"]
          
    def update(self, pos, screen):
        for image in sorted(self.images.items(), key=lambda x: x[1]["layer"]):
            if "clouds" not in image[0]:
                screen.blit(image[1]["image"], image[1]["pos"])
            else:
                image[1]["pos"][0] = -(width+self.dist-self.cloud_speed) if image[1]["pos"][0]+self.cloud_speed > width+self.dist else image[1]["pos"][0]+self.cloud_speed
                screen.blit(image[1]["image"], image[1]["pos"])

        self.play_button.update(screen, pos)
        self.settings_button.update(screen, pos)





clock = pygame.time.Clock()
width, height = 1200,800
screen = pygame.display.set_mode((width,height), flags=pygame.FULLSCREEN)

pygame.mixer.init()
pygame.mixer.music.load('data/music/main-1/main-3.mp3')
pygame.mixer.music.play(-1)

menu = MenuScreen()
#pygame.image.save(screen, "data/menu_images/composite_menu.png")

mouse = pygame.image.load("data/mouse3.png")
mouse = pygame.transform.scale_by(mouse, 4).convert_alpha()
mouse.set_colorkey((255, 255, 255))
mouse_rect = mouse.get_rect()

pygame.mouse.set_visible(False)

while True:
    screen.fill((0,0,0))
    clock.tick(60)

    pygame.display.set_caption((str(clock.get_fps())))

    pos = pygame.mouse.get_pos()
    dx = (width//2-pos[0])/width

    for key, item in menu.images.items():
        if key != "title" and "clouds" not in key:
            item["pos"] = [item["original_pos"][0] + dx*menu.dist/2*item["parallax"], item["original_pos"][1]]


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    menu.update(pos, screen)

    mouse_rect.center = pos
    screen.blit(mouse, mouse_rect)

    pygame.display.flip()