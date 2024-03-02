import pygame

from scripts.entities.entity import Entity
from scripts.utils.core_functions import collision_list, get_images, prep_image, angle_to
from scripts.entities.sword import Sword
from scripts.rendering.animation import Animation, AnimationFade
from scripts.entities.shadow import Shadow

class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self, 6, layer=3)

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

        self.radius = self.rect.width // 2

        masks = [pygame.mask.from_surface(x).to_surface() for x in frames]
        for mask in masks:
            mask.set_colorkey((0,0,0))
        

        draw_pos = (self.rect.bottomleft[0], self.rect.topleft[1] + self.rect.height)
        self.anims = {"walk":Animation(frames[0:5], self.fps, draw_pos, self.layer, loop=True, alive=False), 
                      "idle":Animation(frames[5:], self.fps, draw_pos, self.layer, loop=True, alive=False),
                      "walk_mask":Animation(masks[0:5], self.fps, draw_pos, self.layer, loop=True, alive=False, blank=True),
                      "idle_mask":Animation(masks[5:], self.fps, draw_pos, self.layer, loop=True, alive=False, blank=True)}
        
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

        self.dash_whoosh = pygame.mixer.Sound("data/sound_effects/dash.wav")

        self.shadow = Shadow([0,0,self.rect.width,16], 0.9)

        self.health = 15
        self.is_alive = True
        self.invincibility_timer_max = 15
        self.invincibility_timer_dash = self.dash_frames + 3
        self.invincibility_timer = 0

        self.knockback_timer_max = 5
        self.knockback_timer = self.knockback_timer_max
        self.knockback_vel = pygame.Vector2(0,0)

        self.zeal = 0
        self.zeal_max = 99

        self.death_sound = pygame.mixer.Sound("data/sound_effects/player_death_01.wav")

    def set_HUD(self, HUD):
        self.HUD = HUD
        
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
            self.invincibility_timer = self.invincibility_timer_dash
            self.dash_whoosh.play()

    def take_damage(self, damage, projectile):
        if self.invincibility_timer <= 0:        
            self.health -= damage
            self.HUD.flash(damage)

            self.invincibility_timer = self.invincibility_timer_max

            self.knockback_vel = projectile.vel
            self.knockback_timer = self.knockback_timer_max

    def gain_zeal(self):
        self.zeal = min(self.zeal+11, self.zeal_max)


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
        if self.vel == [0,0]:
            if not (self.state == "idle" or self.state == "idle_mask"):
                self.anims[self.state].stop()

            if self.invincibility_timer > 0:
                if self.state == "idle":
                    self.anims[self.state].stop()
                self.state = "idle_mask"
            else:
                if self.state == "idle_mask":
                    self.anims[self.state].stop()
                self.state = "idle" 
        else:
            if not (self.state == "walk" or self.state == "walk_mask"):
                self.anims[self.state].stop()

            if self.invincibility_timer > 0:
                if self.state == "walk":
                    self.anims[self.state].stop()
                self.state = "walk_mask"
            else:
                if self.state == "walk_mask":
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

    def handle_invincibility(self):
        if self.invincibility_timer > 0:
            self.invincibility_timer -= 1

    def handle_knockback(self):
        if self.knockback_timer > 0:
            self.vel = self.knockback_vel

            self.knockback_timer -= 1

    def update(self, obstacles, camera, pos):

        self.handle_key_presses()

        self.handle_knockback()

        self.move(obstacles)
        self.pos = (self.rect.midtop[0] + camera.rect.x, self.rect.midtop[1] + camera.rect.y) # Maybe port into entity move class later

        self.make_dash_fade(camera)
        self.handle_invincibility()
        self.get_state()
        self.get_facing(pos)
        self.anim_player()

        if self.health <= 0:
            if self.is_alive:
                self.is_alive = False
                pygame.mixer.music.fadeout(30)
                pygame.mixer.stop()
                self.death_sound.play()



        #pygame.draw.rect(camera.display, (255, 0, 0), self.rect)
        
        # Send to be handled at camera z order render layer, remove redundance and implement elegance
        self.sword.update(pos, camera)
        self.shadow.update((self.rect.left, self.rect.bottom - 10), camera)


