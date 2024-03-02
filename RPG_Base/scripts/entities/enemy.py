import pygame
import math
import pytweening
import random

from scripts.entities.entity import Entity
from scripts.utils.core_functions import prep_image, angle_to, collision_list, distance, get_images
from scripts.vfx.particles import Spark, part_handler, explosion
from scripts.entities.projectile import proj_handler, ProjectileCircle, ProjectileHoming

# Enemies need (generic) speed, health, damage
# (specific) animation, special attacks, 

class Enemy(Entity):
    def __init__(self, speed):
        Entity.__init__(self, speed=speed, layer=1)

        self.health = 100
        self.is_alive = True

        self.los = False
        self.last_seen = [0,0]

        enemy_handler.add_enemy(self)

    def move_to(self, pos):
        angle = math.radians(angle_to(self.pos, pos))
        #print(angle)

        #if distance(self.rect.center, pos) > 50:
        self.vel = pygame.Vector2(math.cos(angle), math.sin(angle))

    def line_of_sight(self, player, obstacles, camera):
        for obstacle in obstacles:
            if obstacle.rect.clipline((self.pos, player.pos)):
                if self.los == True:
                    self.last_seen = list(player.pos)
                self.los = False
                break
        else: # if the los is unobstructed
            #if self.los == False: # if previously obstructed
                #self.last_seen = list(player.pos)
            self.los = True
        
        #color = (255,0,0)
        #if self.los:
            #color = (0,255,0)
        #pygame.draw.line(camera.display, color, self.pos, player.pos)

    def find_walls(self, obstacles, camera):
        walls = []
        for obstacle in obstacles:
            dist = distance(obstacle.rect.center, self.pos)
            if dist < 3*self.rect.width:
                #pygame.draw.line(camera.display, (255,0,0), self.pos, obstacle.rect.center)
                angle = math.radians(angle_to(self.pos, obstacle.rect.center))
                walls.append([dist, angle])

        return walls
        

    def pathfind(self, target, obstacles, camera, enemies):
        self.line_of_sight(target, obstacles, camera)
        walls = self.find_walls(obstacles, camera)

        wall_weight = 6
        target_weight = 10
        clump_weight = 200

        if self.los:
            angle = math.radians(angle_to(self.pos, target.pos))
            dist_to_target = distance(target.rect.center, self.pos)
        if not self.los:
            angle = math.radians(angle_to(self.pos, self.last_seen))
            dist_to_target = distance(self.pos, self.last_seen)

        #pygame.draw.circle(camera.display, (0,0,255), self.last_seen, 15)

        
        target_vector = pygame.Vector2(0,0)
        if dist_to_target > 100 : #magic
            target_vector = pygame.Vector2(math.cos(angle), math.sin(angle))*target_weight
       
        #anti_clump = -pygame.Vector2(math.cos(angle), math.sin(angle))*1/(dist_to_target)*1000


        wall_vector = pygame.Vector2(0,0)
        if dist_to_target > 100:
            for dist, angle in walls:
                wall_vector[0] -= math.cos(angle) * 1/dist
                wall_vector[1] -= math.sin(angle) * 1/dist

        clump_vector = pygame.Vector2(0,0)
        for enemy in enemies:
            angle = math.radians(angle_to(self.pos, enemy.pos)) 
            dist = distance(self.pos, enemy.pos)
            if dist < 100 and enemy != self and dist_to_target > 100:
                clump_vector[0] -= math.cos(angle) * 1/max(0.1,dist)
                clump_vector[1] -= math.sin(angle) * 1/max(0.1,dist)

        if wall_vector != [0,0]:
            wall_vector = wall_vector.normalize()*wall_weight

        if clump_vector != [0,0]:
            clump_vector = clump_vector.normalize()*clump_weight
        
        self.vel = (target_vector + wall_vector + clump_vector)#+ anti_clump)
        if self.vel != [0,0]:
            self.vel = self.vel.normalize()


class Wendigo(Enemy):
    def __init__(self, x, y, config=None):
        Enemy.__init__(self, speed=3)

        self.pos = pygame.Vector2(x,y)

        self.layer = 2

        #=== Internal timing circuit ===#
        self.t = 0
        
        #=== Image Handling ===#
        images = [prep_image(x, 4) for x in get_images("data/wendigo_exp.png")]
        self.img = images[2]
        self.rect = self.img.get_frect(x=x, y=y)

        self.hands = (images[0], images[1])
        self.hand_rect = self.hands[0].get_rect()
        self.update_hands()

        #=== Image Masks =====#
        self.body_mask = pygame.mask.from_surface(self.img)
        self.body_mask = self.body_mask.to_surface()
        self.body_mask.set_colorkey((0,0,0))

        self.hand_masks = []
        for hand in self.hands:
            mask = pygame.mask.from_surface(hand)
            mask = mask.to_surface()
            mask.set_colorkey((0,0,0))
            self.hand_masks.append(mask)


        self.radius = 45
        #self.hitbox = pygame.geometry.Circle(self.rect.x, self.rect.y, self.radius)

        self.just_hit_by = []

        #=== Attack Dynamics ===#
        # The blight does two attacks simultaneously:
        # 1) A hand-raise slam attack that shoots out projectiles
        # 2) Also a closer-range area damage that has a chance of hex cursing the player
        self.attacking = False

        self.attack_curve = [12, 5, 22, 22] # windup, approach, impact, recede
        self.attack_timer_max = sum(self.attack_curve)
        self.attack_timer = self.attack_timer_max

        self.hands_draw_pos_y = 0

        self.knockback_timer_max = 20
        self.knockback_timer = self.knockback_timer_max
        self.knockback_vector = pygame.Vector2(0,0)


        self.state = "chase" # idle, recover, die, attack

        self.hit_sound = pygame.mixer.Sound("data/sound_effects/shoot.wav")
        self.death_sound = pygame.mixer.Sound("data/sound_effects/death_02.wav")
        self.death_sound.set_volume(0.4)

        #===== Projectile
        projs = get_images("data/projectile_0.png")
        self.projectile = prep_image(projs[0], 4).convert_alpha()
        self.aoe = prep_image(projs[1], 4).convert_alpha()

        self.facing = False # Start facing left


        # Implement a ticket system to avoid overfilling the screen

    def update_hands(self):
        self.left_hand_pos = [self.rect.centerx - 70, self.rect.centery + math.cos(self.t)*4 + 30]
        self.right_hand_pos = [self.rect.centerx + 70-self.hand_rect.width, self.rect.centery + math.cos(self.t-1)*4 + 30]

    def attack(self):
        if self.state != "attack":
            self.state = "attack"
            self.attack_timer = self.attack_timer_max

    def handle_attack(self, camera, player):
        self.attack_timer -= 1

        if self.attack_timer >= self.attack_timer_max-self.attack_curve[0]: # in the approach phase
            ti = min(1, 1-2*(self.attack_timer - (self.attack_timer_max-self.attack_curve[0]))/(self.attack_timer_max-self.attack_curve[0]))
            self.hands_draw_pos_y = self.left_hand_pos[1] - pytweening.easeInOutQuad(ti)*100

        elif self.attack_timer >= self.attack_timer_max-sum(self.attack_curve[:2]): # in the pause phase
            pass

        elif self.attack_timer >= self.attack_timer_max-sum(self.attack_curve[:3]): # in the attack phase
            self.hands_draw_pos_y = self.left_hand_pos[1]+20

            if self.attack_timer == self.attack_timer_max-sum(self.attack_curve[:2])-1:
                num_proj = 8
                offset = random.randint(0,30)

                camera.set_screen_shake(30)

                for i in range(num_proj):
                    angle = math.radians(i*360/num_proj+offset)
                    proj_handler.add_projectile(ProjectileCircle(self.rect.center, 5, (math.cos(angle), math.sin(angle)), 10, 
                                                                 lifetime=12000, img=self.projectile,origin="enemy"))
                    
                #proj_handler.add_projectile(ProjectileCircle([self.rect.centerx, self.rect.centery+60], 0, (0,0), 50, 
                                                                 #lifetime=12, img=self.aoe,origin="enemy", layer=0.9))
                self.hit_sound.play()


        elif self.attack_timer <= 0: # in the recovery phase
            self.state = "chase"

    def draw_hands(self, camera):
        # Clean the code up here
        if self.state == "attack":
            camera.display.blit(self.hands[0], (self.left_hand_pos[0], self.hands_draw_pos_y))
            camera.display.blit(self.hands[1], (self.right_hand_pos[0], self.hands_draw_pos_y))
        elif self.state == "recover":
            camera.display.blit(self.hand_masks[0], self.left_hand_pos)
            camera.display.blit(self.hand_masks[1], self.right_hand_pos)
        else:
            camera.display.blit(self.hands[0], self.left_hand_pos)
            camera.display.blit(self.hands[1], self.right_hand_pos)

    def move_camera(self, camera, dx, dy):
        # Send out to external function later
        self.rect.x -= int(dx * camera.speed)
        self.rect.y -= int(dy * camera.speed)

        self.last_seen[0] -= int(dx * camera.speed)
        self.last_seen[1] -= int(dy * camera.speed)

        self.hands_draw_pos_y -= int(dy * camera.speed)


    def take_hit(self, projectile, player):
        if projectile not in self.just_hit_by:
            self.just_hit_by.append(projectile)
            self.health -= projectile.damage

            angle = math.radians(angle_to(self.pos, player.pos))
            self.vel = -pygame.Vector2(math.cos(angle), math.sin(angle))

            self.state = "recover"
            self.knockback_timer = self.knockback_timer_max

    def knockback(self):
        t = min(1,(self.knockback_timer_max - self.knockback_timer)/self.knockback_timer_max)
        self.speed = (1-pytweening.easeOutQuart(t))*30

    def knockback_sparks(self, particle_handler):
        _, angle = self.vel.as_polar()
        for i in range(-2,3):
            particle_handler.add_particle(Spark(list((self.pos, self.rect.center[1]+60)), 
                                                math.radians(30)*i+math.radians(angle), 7, (235,235,235), target=self))

    def handle_death(self):
        self.death_sound.play()
        explosion(self.rect.center, 20, part_handler)

    def update(self, camera, player, obstacles, enemies):

        self.update_clock()
        self.update_hands()

        if not player.is_alive:
            self.state = "idle"
            self.vel = pygame.Vector2(0,0)

        if self.state == "attack":
            self.handle_attack(camera, player)
            self.vel = pygame.Vector2(0,0)

        elif self.state == "chase":
            self.pathfind(player, obstacles, camera, enemies)

            if distance(self.pos, player.pos) < 300 and self.los:
                self.attack()

        elif self.state == "recover":
            self.knockback_timer -= 1
            if self.knockback_timer > 0:
                self.knockback()
                #if self.knockback_timer == self.knockback_timer_max-3:
                    #self.knockback_sparks(particle_handler)
            else:
                self.state = "chase"
                self.speed = self.MAXSPEED        

        # get rid of projectiles that have already hit the enemy
        for projectile in reversed(self.just_hit_by):
            if not projectile.is_alive:
                self.just_hit_by.remove(projectile)

        self.move(obstacles)

        self.facing = self.rect.x - player.rect.x < 0

        self.pos[0] = self.rect.centerx + camera.rect.x
        self.pos[1] = self.rect.centery + camera.rect.y

        if self.health <= 0:
            self.handle_death()
            self.is_alive = False

        else:       
            camera.to_render(self)

    def update_clock(self):
        self.t = self.t+0.1%math.pi

    def draw(self, camera):
        
        self.draw_hands(camera)

        if self.state == "recover":
            camera.display.blit(pygame.transform.flip(self.body_mask, self.facing, False).convert_alpha(), self.rect)
        else:
            camera.display.blit(pygame.transform.flip(self.img, self.facing, False).convert_alpha(), self.rect)

        #pygame.draw.circle(camera.display, (200,200,200), self.rect.center, self.radius, 2)
        #pygame.draw.line(camera.display, (255,0,0), self.rect.center, (self.rect.center[0] + self.vel[0]*50,self.rect.center[1] + self.vel[1]*50), 10)
        #pygame.draw.rect(camera.display, (100,100,100), self.rect)
            
class EnemyHandler():
    def __init__(self):
        self.enemy_list = []

    def add_enemy(self, enemy):
        self.enemy_list.append(enemy)

    def update(self, camera, dx, dy, obstacles, player):
        # reversed iteration for efficient removal

        for enemy in reversed(self.enemy_list):
            enemy.move_camera(camera, dx, dy)
            enemy.update(camera, player, obstacles, self.enemy_list)

            if not enemy.is_alive:
                self.enemy_list.remove(enemy)
                enemy.kill()

            else:
                for obstacle in obstacles:
                    if obstacle.rect.collidepoint(enemy.pos):
                        self.enemy_list.remove(enemy)
                        del enemy
                        break
                else:
                    camera.to_render(enemy)

enemy_handler = EnemyHandler()