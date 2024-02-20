import pygame

from scripts.utils.core_functions import blitRotateCenter

# To play an animation, simply pass it to the animation handler

class Animation():
    '''Base class for handling animated sprites (with keyframes)'''

    def __init__(self, frames, framerate, pos, layer=1, static=False, loop=False, alive=False):
        self.frames = frames
        self.frame = 0
        self.framerate = framerate
        self.pos = pos

        self.alive = alive
        self.loop = loop

        self.facing_h = False
        self.facing_v = False

        self.layer = layer

        self.rect = pygame.Vector2(pos)


    def draw(self, camera):
        camera.display.blit(pygame.transform.flip(self.frames[int(self.frame)%len(self.frames)], 
                                                  self.facing_h, self.facing_v), self.pos)

    def set_frame(self, frame):
        '''Access a specific frame in the animation sequence'''
        self.frame = min(max(frame, 0), len(self.frames))

    def set_pos(self, pos):
        self.pos = pos

    def set_facing(self, horiz=False, vert=False):
        self.facing_h = horiz
        self.facing_v = vert

    def set_layer(self, layer):
        self.layer = layer

    def play(self):
        '''Playing an animation simply adds it to the animation handling queue'''
        if not self.alive:
            self.alive = True
            anim_handler.add_animation(self)

    def stop(self):
        self.alive = False

    def kill(self):
        pass

    def advance(self):
        if (self.frame + self.framerate) >= len(self.frames):
            self.frame = 0

            if not self.loop:
                self.alive = False

        else:
            self.frame += self.framerate

class AnimationRotation(Animation):
    '''Variation of Animation class, including the capacity to rotate sprites'''

    def __init__(self, frames, framerate, pos, angle, layer=0, static=False):
        Animation.__init__(self, frames, framerate, pos, layer=0, static=False)

        self.angle = angle

    def set_angle(self, angle):
        self.angle = angle

    def draw(self, camera):
        blitRotateCenter(camera.display, self.frames[int(self.frame)%len(self.frames)], self.pos, self.angle)


class AnimationFade(Animation):
    def __init__(self, img, pos, duration, camera_pos, starting_alpha=255, layer=2, kill_self=True):
        Animation.__init__(self, None, None, pos, layer=layer)
        self.img = img
        self.pos = pos
        self.duration = duration
        self.fade_rate = 255//duration

        self.starting_alpha = starting_alpha
        self.alpha = starting_alpha

        self.camera_pos = camera_pos

        self.alive = False
        self.kill_self = kill_self

        anim_handler.add_animation(self)

    def get_pos(self, camera):
        d_cx = camera.x - self.camera_pos[0]
        d_cy = camera.y - self.camera_pos[1]
        return (self.pos[0]-d_cx, self.pos[1]-d_cy)
    
    def track(self, camera):
        self.camera_pos = (camera.x, camera.y)
    
    def draw(self, camera):
        img = self.img
        img.set_alpha(self.alpha)
        camera.display.blit(img, self.get_pos(camera))

    def reset_anim(self):
        self.alpha = self.starting_alpha

    def kill(self):
        if self.kill_self:
            del self

    def advance(self):
        self.duration -= 1
        self.alpha -= self.fade_rate

        if self.duration <= 0:
            self.alive = False
            
class AnimationHandler():
    '''Handles animations for the entire game'''
    
    def __init__(self):
        self.anims = []

    def add_animation(self, anim):
        self.anims.append(anim)

    def update(self, camera):
        for anim in reversed(self.anims):
            anim.advance() # maybe deltatime?

            if not anim.alive:
                self.anims.remove(anim)
                anim.kill()

            else:
                camera.to_render(anim)

anim_handler = AnimationHandler()

