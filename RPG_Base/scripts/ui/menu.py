import pygame, sys

from scripts.ui.button import Button

class MenuScreen():
    def __init__(self, width, height, camera, clock, mouse, screen):
        
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

        self.play_button = Button("data/menu_images/start.png", (60,350), scale=1.00, 
                                  hover_sound="data/sound_effects/heartbeat_hover.wav")
                                  #selected_sound="data/sound_effects/player_death_01.wav")
        self.settings_button = Button("data/menu_images/settings.png", (60,575), scale=1.00, 
                                      hover_sound="data/sound_effects/heartbeat_hover.wav")
                                      #selected_sound="data/sound_effects/tone_01_E.wav")


        self.width = width
        self.height = height

        self.load_images()

        fade_out = pygame.surface.Surface((width, height))
        fade_out.fill((0,0,0))
        fade_out.set_alpha(0)
        self.fade_out = fade_out
        self.fade_t = 0

        pygame.mixer.music.load('data/music/main-1/main-3.mp3')
        pygame.mixer.music.play(-1)

        self.camera = camera
        self.clock = clock
        self.mouse = mouse
        self.screen = screen

        camera.vignette = 0.9
   
    
    def load_images(self):
        for image_name, image_data in self.images.items():
            if image_name == "title":
                image_data["image"] = pygame.transform.scale_by(image_data["image"], 0.8).convert_alpha()
            elif image_name == "sky" or image_name == "castle":
                image_data["image"] = pygame.transform.scale(image_data["image"], (self.width, self.height)).convert_alpha()
            else:
                img_width, _ = image_data["image"].get_size()
                factor = (self.width+self.dist)/img_width
                image_data["image"] = pygame.transform.scale_by(image_data["image"], factor).convert_alpha()
                img_width, img_height = image_data["image"].get_size()

                if image_name == "clouds_1":
                    image_data["pos"] = [0, 0]
                elif image_name == "clouds_2":
                    image_data["image"] = pygame.transform.flip(image_data["image"], True, False).convert_alpha()
                    image_data["pos"] = [img_width, 0]
                else:
                    image_data["pos"] = [-self.dist//2, self.height-img_height]
            
            image_data["original_pos"] = image_data["pos"]

    def parallax(self):
        pos = pygame.mouse.get_pos()
        dx = (self.width//2-pos[0])/self.width
        for key, item in self.images.items():
            if key != "title" and "clouds" not in key:
                item["pos"] = [item["original_pos"][0] + dx*self.dist/2*item["parallax"], item["original_pos"][1]]
          
    def update(self, pos, camera, state):
        screen = camera.display
        self.parallax()
        for image in sorted(self.images.items(), key=lambda x: x[1]["layer"]):
            if "clouds" not in image[0]:
                screen.blit(image[1]["image"], image[1]["pos"])
            else:
                image[1]["pos"][0] = -(self.width+self.dist-self.cloud_speed) if image[1]["pos"][0]+self.cloud_speed > self.width+self.dist else image[1]["pos"][0]+self.cloud_speed
                screen.blit(image[1]["image"], image[1]["pos"])

        self.play_button.update(screen, pos)
        self.settings_button.update(screen, pos)

        if self.play_button.selected:
            self.fade_t = min(255, self.fade_t+2)
            self.fade_out.set_alpha(self.fade_t)
            screen.blit(self.fade_out, (0,0))

            #pygame.mixer.music.fadeout(1020)

            if self.fade_t >= 254:
                state = "transition"

        return state

    def run(self, state):
        self.screen.fill((0,0,0))
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

        out_state = self.update(pos, self.camera, state)

        self.mouse.update(self.camera)

        #screen.blit(fade_out, (0,0))
        self.camera.draw_world()
        self.camera.update()

        return out_state
