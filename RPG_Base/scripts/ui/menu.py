import pygame, sys

pygame.init()

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
                "pos": [0,0]
            }
        }

        self.cloud_speed = 1

        self.dist = 50
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
            
          
    def update(self, screen):
        for image in sorted(self.images.items(), key=lambda x: x[1]["layer"]):
            if "clouds" not in image[0]:
                screen.blit(image[1]["image"], image[1]["pos"])
            else:
                image[1]["pos"][0] = -(width+self.dist-self.cloud_speed) if image[1]["pos"][0]+self.cloud_speed > width+self.dist else image[1]["pos"][0]+self.cloud_speed
                screen.blit(image[1]["image"], image[1]["pos"])




clock = pygame.time.Clock()
width, height = 1200,800
screen = pygame.display.set_mode((width,height))

pygame.mixer.init()
pygame.mixer.music.load('data/music/main-1/main-2.mp3')
pygame.mixer.music.play(-1)

menu = MenuScreen()

menu.update(screen)
pygame.image.save(screen, "data/menu_images/composite_menu.png")


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

    menu.update(screen)

    pygame.display.flip()