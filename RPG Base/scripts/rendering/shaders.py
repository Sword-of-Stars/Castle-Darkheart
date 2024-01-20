import sys
from array import array

import pygame
import moderngl

class ShaderContext():
    def __init__(self):
        self.ctx = moderngl.create_context()

        self.quad_buffer = self.ctx.buffer(data=array('f', [
            # position (x, y), uv coords (x, y)
            -1.0, 1.0, 0.0, 0.0,  # topleft
            1.0, 1.0, 1.0, 0.0,   # topright
            -1.0, -1.0, 0.0, 1.0, # bottomleft
            1.0, -1.0, 1.0, 1.0,  # bottomright
        ]))

        self.program = self.ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
        self.render_object = self.ctx.vertex_array(self.program, [(self.quad_buffer, '2f 2f', 'vert', 'texcoord')])

        self.time = 0

    def surf_to_texture(self,surf):
        tex = self.ctx.texture(surf.get_size(), 4)
        tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        tex.swizzle = 'BGRA'
        tex.write(surf.get_view('1'))
        return tex

    def update(self, display):
        self.time += 1

        frame_tex = self.surf_to_texture(display)
        frame_tex.use(0)
        self.program['tex'] = 0
        #self.program['time'] = 0#self.time
        self.render_object.render(mode=moderngl.TRIANGLE_STRIP)
        
        pygame.display.flip()
        
        frame_tex.release()

vert_shader = '''
#version 330 core

in vec2 vert;
in vec2 texcoord;
out vec2 uvs;

void main() {
    uvs = texcoord;
    gl_Position = vec4(vert, 0.0, 1.0);
}
'''

frag_shader = '''
#version 330 core

uniform sampler2D tex;

in vec2 uvs;
out vec4 f_color;

void main() {
    f_color = vec4(texture(tex, uvs).rg, texture(tex, uvs).b, 1.0);
}
'''