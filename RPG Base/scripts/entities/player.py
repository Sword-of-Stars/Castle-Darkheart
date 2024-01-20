import pygame

from scripts.entities.entity import Entity
from scripts.utils.core_functions import collision_list, get_images, prep_image
from scripts.entities.sword import Sword
from scripts.rendering.animation import Animation, AnimationFade

class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self, 6, layer=1)

        # TODO: Generalize and store to config for flexi/scalability

        # Key Presses and Movement
        self.pressed = {"right":False, "left":False, "up":False,"down":False, "space":False}
        self.most_recent_press = {"horizontal":'',"vertical":''}

        # Animation handling
        self.state = "idle"
        self.facing = 0
        self.fps = 1/8

        frames = [prep_image(image, 4) for image in get_images("data/knight5.png")]
        self.rect = frames[0].get_frect(x=x, y=y+40)
        self.orig_rect = self.rect.copy()
        self.rect.height -= 40
        self.pos = self.rect.midbottom

        draw_pos = (self.rect.bottomleft[0], self.rect.topleft[1] + self.rect.height)
        self.anims = {"idle":Animation(frames[0:5], self.fps, draw_pos, self.layer, loop=True, alive=False), 
                      "walk":Animation(frames[5:], self.fps, draw_pos, self.layer, loop=True, alive=False)}
        
        # Speed and Movement
        self.speed = 6
        self.normal_speed = 6

        # Dashing
        self.dashing = False # But I'm always dashing
        self.dash_speed = 30
        self.dash_frames = 8
        self.dash_timer = 0
        self.MAX_DASH_TIMER = 100

        self.sword = Sword(self)

        self.mask = pygame.mask.from_surface(frames[0])
        self.mask = self.mask.to_surface()
        self.mask.set_colorkey((0,0,0))
        

    def handle_key_presses(self):
        # Set the player's speed to 0 (may not be necessary)
        self.vel = pygame.Vector2(0,0) 

        # Respond to key presses
        if self.pressed["right"] and self.most_recent_press["horizontal"] != "left":
            self.vel[0] = 1
        elif self.pressed["left"] and self.most_recent_press["horizontal"] != "right":
            self.vel[0] = -1

        if self.pressed["up"] and self.most_recent_press["vertical"] != "down":
            self.vel[1] = -1
        elif self.pressed["down"] and self.most_recent_press["vertical"] != "up":
            self.vel[1] = 1

        if self.pressed["space"]:
            self.dash()

    def get_facing(self, pos):
        """Have the player always facing the cursor"""

        # Facing right
        if pos[0] > self.rect.x:
            self.facing = 1
        # Facing left
        else:
            self.facing = 0

    def handle_dash(self):
        self.dash_timer -= 1

        if self.dashing:

            # If the player should still be dashing
            if self.dash_timer >= self.MAX_DASH_TIMER:
                self.speed = self.dash_speed
            
            # Otherwise, 
            elif self.dash_timer <= self.MAX_DASH_TIMER:
                self.dashing = False
                self.speed = self.normal_speed

    def dash(self):
        if self.dash_timer <= 0:
            self.dashing = True
            self.dash_timer = self.MAX_DASH_TIMER + self.dash_frames

    def make_dash_fade(self, camera):
        '''Make the glowing white aftereffects of dashing'''
        if self.dashing:
            if self.dash_timer % 3 == 0:
                # Draw an offset for hitbox
                # BUG: 12 is a magic number
                draw_pos = (self.rect.left, self.rect.top-self.rect.height-12)

                AnimationFade(self.mask, draw_pos, 15, 
                            camera_pos=(camera.x, camera.y)).play()
  
    def normalize_speed(self):
        self.handle_dash()
        if self.vel != [0,0]:
            vx, vy = self.vel.normalize()*self.speed
        else:
            vx, vy = 0,0
        return vx, vy
    
    def get_state(self):
        if self.vel != [0,0]:
            if self.state != "idle":
                self.anims[self.state].stop()
            self.state = "idle" # There's some error with facing and the idle set of animations
        else:
            if self.state != "walk":
                self.anims[self.state].stop()
            self.state = "walk"

    def anim_player(self):
        # Draw an offset for hitbox
        # BUG: 12 is a magic number
        draw_pos = (self.rect.left, self.rect.top-self.rect.height-12)

        self.anims[self.state].set_facing(horiz=self.facing)
        self.anims[self.state].set_pos(draw_pos)
        self.anims[self.state].set_layer(self.layer)
        self.anims[self.state].play()

    def move_camera(self, camera, dx, dy):
        # Send out to external function later
        self.rect.x -= int(dx * camera.speed)
        self.rect.y -= int(dy * camera.speed)

    def update(self, obstacles, camera, pos):

        self.handle_key_presses()

        self.move(obstacles)
        self.pos = (self.rect.midtop[0] + camera.rect.x, self.rect.midtop[1] + camera.rect.y) # Maybe port into entity move class later

        self.make_dash_fade(camera)
        self.get_state()
        self.get_facing(pos)
        self.anim_player()

        #pygame.draw.rect(camera.display, (255, 0, 0), self.rect)
        
        # Send to be handled at camera z order render layer, remove redundance and implement elegance
        self.sword.update(pos, camera)

