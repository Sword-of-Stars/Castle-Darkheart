import pygame

from scripts.entities.entity import Entity

class Projectile(Entity):
    def __init__(self, pos, speed, vel, lifetime=10000, img=None, origin=None):
        Entity.__init__(self, speed, layer=1)

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

    def move(self):
        # You can add pygame vectors, interesting to look into
        self.pos += self.vel

    def update(self):

        self.lifetime -= 1

        if self.lifetime <= 0:
            self.is_alive = False

        else:
            self.move()
            self.rect = self.pos



class ProjectileCircle(Projectile):
    def __init__(self, pos, speed, vel, radius, lifetime=10000, img=None, origin=None):
        Projectile.__init__(self, pos, speed, vel, lifetime, img, origin)

        self.radius = radius

    def draw(self, camera):
        # in future, reassign functions rather than a check every loop
        if self.img != None:
            pygame.draw.circle(camera.display, (255,0,0), self.pos, self.radius)


class ProjectileHandler():
    def __init__(self):
        self.projectile_list = []

    def add_projectile(self, projectile):
        self.projectile_list.append(projectile)

    def update(self, camera):
        # reversed iteration for efficient removal

        for projectile in reversed(self.projectile_list):
            projectile.update()

            if not projectile.is_alive:
                self.projectile_list.remove(projectile)
                projectile.kill()

            else:
                camera.to_render(projectile)

proj_handler = ProjectileHandler()
