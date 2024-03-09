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

    def update(self, display, ui, outRad, inRad): # eventually just use kwargs
        self.time += 1

        frame_tex = self.surf_to_texture(display)
        frame_tex.use(0)

        ui_tex = self.surf_to_texture(ui)
        ui_tex.use(1)

        self.program['tex'] = 0
        self.program['ui_surf'] = 1
        self.program['outRad'] = outRad
        self.program['inRad'] = inRad


        #self.program['time'] = self.time
        self.render_object.render(mode=moderngl.TRIANGLE_STRIP)
        
        pygame.display.flip()
        
        frame_tex.release()
        ui_tex.release()

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
uniform sampler2D ui_surf;
uniform float outRad;
uniform float inRad;

in vec2 uvs;
out vec4 f_color;

void main() {
    // Calculate distance from center (assuming a centered vignette)
    vec2 center = vec2(0.5, 0.5);
    float distanceFromCenter = distance(uvs, center);

    // Adjust radii based on texture dimensions (assuming square texture)
    float textureSize = 1.0; // Replace with actual texture size if known
    float innerRadius = inRad * textureSize;
    float outerRadius = outRad * textureSize;

    // Calculate vignette strength
    float vignetteStrength = smoothstep(innerRadius, outerRadius, distanceFromCenter);

    // Apply vignette to texture color
    vec4 textureColor = texture(tex, uvs);
    f_color = vec4(textureColor.rgb * (1.0 - vignetteStrength), textureColor.a);

    // Don't apply vignette to UI
    vec4 ui_color = texture(ui_surf, uvs);
    if (ui_color.a > 0) {
        f_color = ui_color;
  }
}
'''
'''
frag_shader = 
#version 330 core

uniform sampler2D tex;

in vec2 uvs;
out vec4 f_color;

void main() {
    // Calculate distance from center (assuming a centered vignette)
    vec2 center = vec2(0.5, 0.5);
    float distanceFromCenter = distance(uvs, center);

    // Adjust radii based on texture dimensions (assuming square texture)
    float textureSize = 1.0; // Replace with actual texture size if known
    float innerRadius = 0.2 * textureSize;
    float outerRadius = 0.7 * textureSize;

    // Calculate vignette strength
    float vignetteStrength = smoothstep(innerRadius, outerRadius, distanceFromCenter);

    // Apply vignette to texture color
    vec4 textureColor = texture(tex, uvs);
    f_color = vec4(textureColor.rgb * (1.0 - vignetteStrength), textureColor.a);
  }
'''