import pygame
import math

from scripts.entities.entity import Entity
from scripts.utils.core_functions import prep_image, angle_to, collision_list, distance, get_images

# Enemies need (generic) speed, health, damage
# (specific) animation, special attacks, 

class Enemy(Entity):
    def __init__(self, speed):
        Entity.__init__(self, speed=speed, layer=1)

        self.health = 100

        self.los = False
        self.last_seen = [0,0]

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
        
        color = (255,0,0)
        if self.los:
            color = (0,255,0)
        pygame.draw.line(camera.display, color, self.pos, player.pos)

    def find_walls(self, obstacles, camera):
        walls = []
        for obstacle in obstacles:
            dist = distance(obstacle.rect.center, self.pos)
            if dist < 3*self.rect.width:
                pygame.draw.line(camera.display, (255,0,0), self.pos, obstacle.rect.center)
                angle = math.radians(angle_to(self.pos, obstacle.rect.center))
                walls.append([dist, angle])

        return walls
        

    def pathfind(self, target, obstacles, camera):
        self.line_of_sight(target, obstacles, camera)
        walls = self.find_walls(obstacles, camera)

        

        wall_weight = 6
        target_weight = 10


        if self.los:
            angle = math.radians(angle_to(self.pos, target.pos))
            dist_to_target = distance(target.rect.center, self.pos)
        if not self.los:
            angle = math.radians(angle_to(self.pos, self.last_seen))
            dist_to_target = distance(self.pos, self.last_seen)

        pygame.draw.circle(camera.display, (0,0,255), self.last_seen, 15)

        
        target_vector = pygame.Vector2(0,0)
        if dist_to_target > 100 : #magic
            target_vector = pygame.Vector2(math.cos(angle), math.sin(angle))*target_weight
       
        #anti_clump = -pygame.Vector2(math.cos(angle), math.sin(angle))*1/(dist_to_target)*1000


        wall_vector = pygame.Vector2(0,0)
        if dist_to_target > 100:
            for dist, angle in walls:
                wall_vector[0] -= math.cos(angle) * 1/dist
                wall_vector[1] -= math.sin(angle) * 1/dist

        if wall_vector != [0,0]:
            wall_vector = wall_vector.normalize()*wall_weight
        
        self.vel = (target_vector + wall_vector)#+ anti_clump)
        if self.vel != [0,0]:
            self.vel = self.vel.normalize()


class Wendigo(Enemy):
    def __init__(self, x, y, config=None):
        Enemy.__init__(self, speed=6)

        self.pos = pygame.Vector2(x,y)

        self.layer = 1

        #=== Internal timing circuit ===#
        self.t = 0
        
        #=== Image Handling ===#
        images = [prep_image(x, 4) for x in get_images("data/wendigo_exp.png")]
        self.img = images[2]
        self.rect = self.img.get_frect(x=x, y=y)

        self.hands = (images[0], images[1])
        self.hand_rect = self.hands[0].get_rect()
        self.update_hands()


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


        # Implement a ticket system to avoid overfilling the screen

    def update_hands(self):
        self.left_hand_pos = [self.rect.centerx - 70, self.rect.centery + math.cos(self.t)*4 + 30]
        self.right_hand_pos = [self.rect.centerx + 70-self.hand_rect.width, self.rect.centery + math.cos(self.t-1)*4 + 30]

    def move_camera(self, camera, dx, dy):
        # Send out to external function later
        self.rect.x -= int(dx * camera.speed)
        self.rect.y -= int(dy * camera.speed)

        self.last_seen[0] -= int(dx * camera.speed)
        self.last_seen[1] -= int(dy * camera.speed)

    def take_hit(self, projectile):
        if projectile not in self.just_hit_by:
            self.just_hit_by.append(projectile)
            self.health -= projectile.damage 

    def update(self, camera, player, obstacles):
        #self.hitbox = pygame.geometry.Circle(self.rect.x, self.rect.y, self.radius)

        self.update_clock()
        self.update_hands()

        # get rid of projectiles that have already hit the enemy
        for projectile in reversed(self.just_hit_by):
            if not projectile.is_alive:
                self.just_hit_by.remove(projectile)

        #print(obstacles)
        #self.pathfind(player, obstacles, camera)
        self.move(obstacles)

        self.pos[0] = self.rect.centerx + camera.rect.x
        self.pos[1] = self.rect.centery + camera.rect.y
                
        camera.to_render(self)

    def update_clock(self):
        self.t = self.t+0.1%math.pi

    def draw(self, camera):
        
        camera.display.blit(self.hands[0], self.left_hand_pos)
        camera.display.blit(self.hands[1], self.right_hand_pos)
        camera.display.blit(self.img, self.rect)

        pygame.draw.circle(camera.display, (200,200,200), self.rect.center, self.radius, 2)
        pygame.draw.line(camera.display, (255,0,0), self.rect.center, (self.rect.center[0] + self.vel[0]*50,self.rect.center[1] + self.vel[1]*50), 10)
        #pygame.draw.rect(camera.display, (100,100,100), self.rect)