import math
import random

from scripts.vfx.particles import Spark
from scripts.utils.core_functions import distance, angle_to, circle_collide


def handle_projectiles(proj_handler, enemy_handler, player, partman):
    for proj in reversed(proj_handler.projectile_list):
        for enemy in enemy_handler.enemy_list:
            if circle_collide(proj.pos, proj.radius, enemy.rect.center, enemy.radius):
                if proj.origin != "enemy":
                    if enemy.state != "recover":
                        player.sword.hit()

                        if distance(player.pos,enemy.pos) < 50:
                            dist = 20
                        else:
                            dist = distance(player.pos,enemy.pos)+40
                        angle = math.radians(angle_to(player.pos,enemy.pos))

                        for i in range(-5,6):
                            partman.add_particle(Spark([player.pos[0]+math.cos(angle)*dist, player.pos[1]+math.sin(angle)*dist],
                                                math.radians(15)*i+angle, random.randint(6,8), (235,235,235), scale=2))
                        enemy.take_hit(proj, player)
                    
                    
        else:
            if circle_collide(proj.pos, proj.radius, player.rect.center, player.radius):
                if proj.origin == "enemy":
                    player.take_damage(1, proj)
                    proj.unalive()