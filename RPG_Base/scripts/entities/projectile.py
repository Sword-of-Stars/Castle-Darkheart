import pygame

from scripts.entities.entity import Entity

class Projectile(Entity):
    def __init__(self, pos, speed, vel, lifetime=10000, img=None, origin=None, layer=4):
        Entity.__init__(self, speed, layer=layer)

        self.pos = pygame.Vector2(pos)
        self.rect = self.pos
        self.vel = pygame.Vector2(vel)

        self.img = img

        self.lifetime = lifetime
        self.is_alive = True

        proj_handler.add_projectile(self)

        self.origin = origin

        self.damage = 1

    def draw(self, camera):
        if self.img != None:
            pass

    def kill(self):
        del self

    def unalive(self):
        self.is_alive = False

    def move(self, camera, dx, dy):
        # You can add pygame vectors, interesting to look into
        self.pos += self.vel*self.speed
        self.pos[0] -= int(dx * camera.speed)*0.5
        self.pos[1] -= int(dy * camera.speed)*0.5


        #self.rect[0] = self.pos[0] - int(dx * camera.speed)
        #self.rect[1] = self.pos[1] -int(dy * camera.speed)

    def update(self, camera, dx, dy):

        self.lifetime -= 1

        if self.lifetime <= 0:
            self.is_alive = False

        else:
            self.move(camera, dx, dy)



class ProjectileCircle(Projectile):
    def __init__(self, pos, speed, vel, radius, lifetime=10000, img=None, origin=None, layer=4, damage=1):
        Projectile.__init__(self, pos, speed, vel, lifetime, img, origin, layer=layer)

        self.radius = radius
        self.damage = damage

        if self.img != None:
            self.rect = self.img.get_rect()

    def draw(self, camera):
        # in future, reassign functions rather than a check every loop
        if self.img != None:
            pos = (self.pos[0]-self.rect.width//2, self.pos[1]-self.rect.height//2)
            camera.display.blit(self.img, pos)

        #elif self.img == None:
           # pygame.draw.circle(camera.display, (255,0,0), self.pos, self.radius)



class ProjectileHandler():
    def __init__(self):
        self.projectile_list = []

    def add_projectile(self, projectile):
        self.projectile_list.append(projectile)

    def update(self, camera, dx, dy, obstacles):
        # reversed iteration for efficient removal

        for projectile in reversed(self.projectile_list):
            projectile.update(camera, dx, dy)

            if not projectile.is_alive:
                self.projectile_list.remove(projectile)
                projectile.kill()

            else:
                for obstacle in obstacles:
                    if obstacle.rect.collidepoint(projectile.pos):
                        self.projectile_list.remove(projectile)
                        projectile.kill()
                        break
                else:
                    camera.to_render(projectile)

proj_handler = ProjectileHandler()
