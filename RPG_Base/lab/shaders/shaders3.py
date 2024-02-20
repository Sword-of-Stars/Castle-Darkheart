import sys
import os
from array import array
import pygame
import moderngl

pygame.init()

os.chdir(f"{os.getcwd()}/lab/shaders")

screen = pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)
ctx = moderngl.create_context()

clock = pygame.time.Clock()

img = pygame.image.load('img.png')

# Define vertices and texture coordinates for a full-screen quad
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

# Define fragment shader (with glow effect)
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

# Create program and vertex array
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
    # Clear the screen
    screen.fill((0, 0, 0))
    # Draw the image on the screen
    screen.blit(img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    x, y = pygame.mouse.get_pos()

    # Create texture from the screen surface
    frame_tex = surf_to_texture(screen)
    frame_tex.use(0)
    program['tex'] = 0
    program['glowingPoint'] = (x/800, y/600)
    program['glowRadius'] = 0.2
    program['glowColor'] = (1.0, 0.0, 0.0)
    #program['time'] = t
    
    # Draw the quad
    render_object.render(mode=moderngl.TRIANGLE_STRIP)
    
    # Update the display
    pygame.display.flip()
    
    # Release the texture
    frame_tex.release()
    
    clock.tick(60)
