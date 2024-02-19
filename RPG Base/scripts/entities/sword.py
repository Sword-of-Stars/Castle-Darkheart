import pygame, math
from PIL import Image

from scripts.utils.core_functions import get_images, blitRotate, blitRotateCenter, angle_to, prep_image
from scripts.rendering.animation import AnimationRotation, AnimationFade
from scripts.entities.projectile import ProjectileCircle

# TODO: Move set_pos functionality to utils, it's kinda useful
# TODO: Port weapon-specific shit to config JSON

class Weapon():
    def _init__(self):
        pass

    def hi():
        pass

class Sword(Weapon):
    def __init__(self, player):
        Weapon.__init__(self)
        self.player = player

        # Load sword image and smear images
        self.load_sword_image()

        # Swing Angular Information
        self.angle = 0 # The actual angle of the sword
        self.initial_angle = 135 # Sword initially drawn at 45 degree angle
        self.angle_relative_to_target = 120 # Angle of the sword hilt relative to the target

        self.side = -1 # -1 for left/ccw, 1 for right/cw
        self.length = 60 # Distance from player
        self.pos = self.set_pos(0, self.length)

        # Physics attributes
        self.physics_stop = 120
        self.physics_decay = 1.5
        self.angular_velocity = 0

        self.is_swing = False # is the player currently swinging?
        self.num_cooldown_frames = 8
        self.current_swing_frame = 0

       # Initialize the smear attributes
        self.active_smear = False
        self.smear_animations = []
        self.smear_angle = 0
        self.frame_rate = 1/3

        self.smear_length = 110 # distance from player to smear
        self.smear_pos = self.set_pos(90, self.smear_length)

        self.layer = 1.1

        self.smear_anim = AnimationRotation([prep_image(img, (3,4), (0,0,0)) for img in get_images("data/smears_2.png")],
                                     self.frame_rate, self.smear_pos, self.smear_angle, layer=2)
        
        self.damage_radius = 75
        self.damage_distance = self.length // 2

        self.damage_hitboxes = []

        self.swing_sound = pygame.mixer.Sound("data/sound_effects/sword_slash.wav")
        self.hit_sound = pygame.mixer.Sound("data/sound_effects/hit_02.wav")


        self.special_timer_max = 100
        self.special_timer = 0

        self.shield = prep_image(get_images("data/shield.png")[0], 4)
        self.shield.set_alpha(150)
        self.shield_rect = self.shield.get_rect()
        pos = (self.player.rect.x - self.shield_rect.width, self.player.rect.y - self.shield_rect.height)
        self.shield_anim = AnimationFade(self.shield,pos,self.special_timer_max, (0,0), 150, layer=self.player.layer+1, kill_self=True)

    def load_sword_image(self):
        self.img = pygame.transform.scale_by(pygame.image.load("data/sword_4.png").convert_alpha(), 4)
        self.img.set_colorkey((255,255,255))
        self.rect = self.img.get_rect()

    def hit(self):
        self.hit_sound.play()
        self.player.gain_zeal()

    def special(self):
       
        if self.special_timer <= 0:
            self.special_timer = self.special_timer_max

            pos = (self.player.rect.x - self.shield_rect.width, self.player.rect.y - self.shield_rect.height)
            self.shield_anim = AnimationFade(self.shield,pos,self.special_timer_max, (0,0), 150, layer=self.player.layer+1, kill_self=True)

            self.shield_anim.set_pos(self.player.pos)
            self.shield_anim.play()

    def handle_special_cooldown(self, camera):
        
        #self.shield_anim.reset_anim()
        if self.special_timer > 0:
            self.shield_anim.set_pos((self.player.rect.x - self.shield_rect.width//2 + self.player.rect.width//2, 
                                      self.player.rect.y - self.shield_rect.height//2 - self.player.rect.height//4))
            self.shield_anim.track(camera)

            self.special_timer -= 1

    def render_over(self):
        """
        This function determines whether to draw the sword on top of
        or below the player
        """
        angle = angle_to(self.player.rect.midtop, self.player.sword.pos)

        if self.side == -1:
            if angle < 140 and angle > -40:
                self.layer = 1.1
                return True # Sword on top
            
            self.layer = 0.9
            return False
        else:
            if angle < 20 and angle > -160:
                self.layer = 1
                return False # Sword on bottom
            
            self.layer = 1.1
            return True

    def set_angle(self, pos):

        # Find the angle between the wielder and the sword
        angle = angle_to(self.player.rect.midtop, pos)

        a = angle + (self.angle_relative_to_target*self.side)

        self.damage_angle = a + (self.angular_velocity*self.side*self.is_swing)
        self.pos = self.set_pos(self.damage_angle, self.length)
            
        self.smear_pos = self.set_pos(angle, -self.smear_length)

        self.angle = self.initial_angle - angle 
        self.smear_angle = 180 - angle

    def set_pos(self, angle, length):

        return (self.player.rect.centerx-length*math.cos(math.radians(angle)), 
                self.player.rect.top-length*math.sin(math.radians(angle)))

    def swing(self):

        if not self.is_swing:
            self.swing_sound.play()

            self.is_swing = True
            self.active_smear = True
            self.smear_frame = 0
            self.side *= -1

            self.smear_anim.set_layer(2)
            self.smear_anim.set_angle(self.smear_angle)
            self.smear_anim.set_pos(self.smear_pos)
            self.smear_anim.play()


            # Tweak lifetime
            pos = self.set_pos(-self.smear_angle, 90)
            ProjectileCircle(pos, 0, (0,0), self.damage_radius, lifetime=12, origin=self.player, damage=40)

    def reset_swing(self):

        self.physics_stop = 80
        self.current_swing_frame = 0
        self.is_swing = False

    def handle_swing(self):

        if self.is_swing:

            if self.current_swing_frame <= (self.num_cooldown_frames):
                # If the sword is NOT done swinging
                self.angle -= self.physics_stop*self.side
                self.physics_stop /= self.physics_decay
            else:
                self.reset_swing()

            self.current_swing_frame += 1

    def draw(self, camera):
        blitRotate(camera.display, self.img, self.pos, self.rect.bottomleft, self.angle)

    def update(self, pos, camera):

        #self.render_over()
        self.set_angle(pos)
        self.handle_swing()
        self.handle_special_cooldown(camera)

        camera.to_render(self)

