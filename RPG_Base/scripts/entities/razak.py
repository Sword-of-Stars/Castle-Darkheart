import pygame
import random
import math

from scripts.entities.entity import Entity
from scripts.entities.shadow import Shadow
from scripts.utils.core_functions import prep_image, get_images


class Razak(Entity):
    def __init__(self, pos):
        Entity.__init__(self, 0, 3)

        self.images = [prep_image(x, 4) for x in get_images("data/wraith_exp.png")]
        self.body = self.images[1]
        self.rect = self.body.get_rect()
        self.rect.center = pos
        self.pos = pos

        self.hands = (self.images[0], self.images[2])
        self.hand_rect = self.hands[0].get_rect()
        self.hand_positions = [[],[]]

        self.all_spells = self.images[3:]
        self.spells = self.repopulate_spells()
        self.state = "idle"
        
        self.attack_timer_max = 60
        self.attack_timer = self.attack_timer_max
        self.active_spell = None

        self.glow = prep_image(pygame.image.load("data/radial_gradient.png"), 1)

        self.t = 0

        #self.shadow = Shadow(pygame.rect.Rect(self.rect.left, self.rect.bottom+20, self.rect.width, 12), 12)

    def move_camera(self, camera, dx, dy):
        # Send out to external function later
        self.pos[0] -= int(dx * camera.speed)
        self.pos[1] -= int(dy * camera.speed)

    def repopulate_spells(self):
        spells = {
            "spiral":
                {
                "img":self.all_spells[0], 
                "duration":120,
                "function":0
                },
            "homing":
                {
                "img":self.all_spells[1], 
                "duration":120,
                "function":0
                },
            "linear":
                {
                "img":self.all_spells[2], 
                "duration":120,
                "function":0
                },
            "summon":
                {
                "img":self.all_spells[3], 
                "duration":120,
                "function":0
                },
            "shotgun":
                {
                "img":self.all_spells[4], 
                "duration":120,
                "function":0
                }
            }
        return spells


    def update_hands(self):
        for i, hand in enumerate(self.hands):
            k = 45
            if i == 1:
                x_offset = -k
                y_off = 0.3
            else:
                x_offset = k-self.hand_rect.width
                y_off = 0
            
            self.hand_positions[i] =  [self.rect.centerx + x_offset,
                               self.rect.centery+5*math.sin(self.t+y_off)+10]
            
    def draw_hands(self, screen):
        screen.blit(self.hands[0], self.hand_positions[0])
        screen.blit(self.hands[1], self.hand_positions[1])
           
    def draw_spells(self, screen):
        if len(self.spells) > 0:
            delta = 2*math.pi/len(self.spells)

            for i, spell in enumerate(self.spells):
                screen.blit(self.spells[spell]["img"], (-10+self.rect.centerx + 45*math.cos(self.t+(delta*i)),
                                    20+self.rect.centery + 25*math.sin(self.t+(delta*i))))
    
    def draw_body(self, screen):
        screen.blit(self.body, self.rect)

    def attack(self, screen):
        if self.state != "attack":
            self.state = "attack"
            self.attack_timer = self.attack_timer_max

            self.active_spell = None
            if len(self.spells) > 0:
                self.active_spell = self.spells.pop(random.choice(list(self.spells.keys())))

        else:
            self.attack_timer -= 1
            y_off = -50
            self.hand_positions[0][1] = self.rect.centery + y_off
            self.hand_positions[1][1] = self.rect.centery + y_off

            if self.active_spell != None:
                screen.blit(self.active_spell["img"], (self.rect.centerx-10, self.rect.top-40))

        if self.attack_timer <= 0:
            self.state = "idle"


    def idle(self):
        self.pos[1] += 1*math.cos(self.t)

    def draw(self, camera):
        screen = camera.display

        self.draw_hands(screen)
        self.draw_spells(screen)
        self.draw_body(screen)


    def update(self, camera):
        self.t = self.t+0.1%math.pi

        self.update_hands()


        if self.state == "idle":
            self.idle()
        elif self.state == "attack":
            self.attack()

        self.rect.center = self.pos

        #self.shadow.update([self.rect.left, self.rect.bottom+20], camera)

        camera.to_render(self)
