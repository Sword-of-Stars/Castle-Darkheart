import sys,os
from array import array

import pygame
import moderngl

pygame.init()

os.chdir(f"{os.getcwd()}/lab/shaders")


screen = pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)
display = pygame.Surface((800, 600))
ctx = moderngl.create_context()

clock = pygame.time.Clock()

img = pygame.image.load('img.png')


quad_buffer = ctx.buffer(data=array('f', [
    # position (x, y), uv coords (x, y)
    -1.0, 1.0, 0.0, 0.0,  # topleft
    1.0, 1.0, 1.0, 0.0,   # topright
    -1.0, -1.0, 0.0, 1.0, # bottomleft
    1.0, -1.0, 1.0, 1.0,  # bottomright
]))

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
uniform int time;

in vec2 uvs;
out vec4 f_color;

void main() {
    // Calculate distance from center (assuming a centered vignette)
    vec2 center = vec2(0.5, 0.5);
    float distanceFromCenter = distance(uvs, center);

    // Adjust radii based on texture dimensions (assuming square texture)
    float textureSize = 1.0; // Replace with actual texture size if known
    float innerRadius = 0.2 * textureSize;
    float outerRadius = 0.8 * textureSize + 0*time;

    // Calculate vignette strength
    float vignetteStrength = smoothstep(innerRadius, outerRadius, distanceFromCenter);

    // Apply vignette to texture color
    vec4 textureColor = texture(tex, uvs);
    f_color = vec4(textureColor.rgb * (1.0 - vignetteStrength), textureColor.a);
}
'''

frag_shader = '''
#version 330 core

uniform sampler2D tex;
uniform float time;

in vec2 uvs;
out vec4 f_color;

void main() {
    // Calculate distance from center (assuming a centered vignette)
    vec2 center = vec2(0.5, 0.5);
    float distanceFromCenter = distance(uvs, center);

    // Adjust radii based on texture dimensions (assuming square texture)
    float textureSize = 1.0; // Replace with actual texture size if known
    float innerRadius = 0.2 * textureSize;
    float outerRadius = 0.8 * textureSize;

    // Calculate vignette strength
    float vignetteStrength = smoothstep(innerRadius, outerRadius, distanceFromCenter);

    // Toggle between red and black with respect to time
    float colorToggle = abs(sin(time*0.01));
    vec3 color = mix(vec3(0.0), vec3(1.0, 0.0, 0.0), colorToggle); // Red color

    // Apply vignette to texture color
    vec4 textureColor = texture(tex, uvs);
    f_color = vec4(textureColor.rgb * (1.0 - vignetteStrength) + color * vignetteStrength, textureColor.a);
}
'''

frag_shader = '''
#version 330 core

uniform sampler2D tex; // Input texture
uniform vec2 glowingPoint; // Inputted point
uniform float glowRadius; // Radius of the glow
uniform vec3 glowColor; // Color of the glow

in vec2 uvs;
out vec4 f_color;

void main() {
    // Sample the texture
    vec4 textureColor = texture(tex, uvs);

    // Calculate distance from the current fragment to the glowing point
    float distanceToPoint = distance(uvs, glowingPoint);

    // Calculate the glow intensity based on distance
    float glowIntensity = 1.0 - smoothstep(glowRadius - 0.1, glowRadius + 0.1, distanceToPoint);

    // Apply glow color and intensity
    vec3 glow = glowColor * glowIntensity;

    // Mix the texture color with the glow effect
    vec3 finalColor = textureColor.rgb + glow;

    f_color = vec4(finalColor, textureColor.a);
}


'''

#f_color = vec4(texture(tex, uvs).rg, texture(tex, uvs).b*sin(time*0.01), 1.0);
program = ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
render_object = ctx.vertex_array(program, [(quad_buffer, '2f 2f', 'vert', 'texcoord')])

def surf_to_texture(surf):
    tex = ctx.texture(surf.get_size(), 4)
    tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
    tex.swizzle = 'BGRA'
    tex.write(surf.get_view('1'))
    return tex

t = 0

while True:
    display.fill((0, 0, 0))
    display.blit(img, (0,0))

    pygame.display.set_caption(str(clock.get_fps()))
    
    t += 1
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    frame_tex = surf_to_texture(display)
    frame_tex.use(0)
    program['tex'] = 0
    #program['time'] = t
    program['glowingPoint'] = (100,100)
    program['glowRadius'] = 30
    program['glowColor'] = (1.0,0,0)
    render_object.render(mode=moderngl.TRIANGLE_STRIP)
    
    pygame.display.flip()
    
    frame_tex.release()
    
    clock.tick(60)
    