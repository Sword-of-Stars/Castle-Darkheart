import pygame
import random

from array import array

import moderngl

# Define the path to your custom font file
FONT_PATH = "data/fonts/oldenglish.ttf"

# Initialize pygame and create a window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1200, 800), pygame.OPENGL | pygame.DOUBLEBUF)
pygame.display.set_caption("Castle Darkheart: Menu Screen")

clock = pygame.time.Clock()

# Load the custom font
font = pygame.font.Font(FONT_PATH, 128)
font2 = pygame.font.Font(FONT_PATH, 32)


# Render some text with the custom font
color = (244, 255, 255)
ts1 = font.render("Castle", True, color)
ts2 = font.render("Darkheart", True, color)
ts3 = font2.render("v1.0", True, color)


#text_surface = pygame.transform.scale2x(text_surface)

img = pygame.image.load("data/menu_screen.png").convert_alpha()
img = pygame.transform.scale_by(img, 5)

clouds = pygame.image.load("data/clouds.png").convert_alpha()
clouds = pygame.transform.scale_by(clouds, 5)


cloud_list = [clouds for i in range(5)]
y_vals = [random.randint(0,400) for i in range(5)]
x_start = [random.randint(-300, 1200) for i in range(5)]
speeds = [random.random() for i in range(5)]

disp = pygame.surface.Surface((1200,800))

# Load the MP3 file
pygame.mixer.music.load("data/music/main-1/dgv_03.mp3")

# Play the music

class Button:
    def __init__(self, x, y, width, height, text_color=(255, 255, 255), 
                 hover_color=(200, 200, 200), font_size=30, text="",
                 image_path=None, hover_sound=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text_color = text_color
        self.hover_color = hover_color
        self.font_size = font_size
        self.text = text
        self.image_path = image_path
        self.hover_sound = pygame.mixer.Sound(hover_sound)
        self.font = pygame.font.Font(None, self.font_size)
        self.rect = pygame.Rect(x, y, width, height)
        self.hovered = False

    def update(self, mouse_pos, disp):
        self.hovered = self.rect.collidepoint(mouse_pos)
        if self.hovered:
            self.hover_sound.play()

        self.draw(disp)

    def draw(self, screen):
        if self.image_path:
            image = pygame.image.load(self.image_path)
            screen.blit(image, (self.x, self.y))
        else:
            color = self.hover_color if self.hovered else self.text_color
            pygame.draw.rect(screen, color, self.rect, 2)  # Draw border
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

        # Move button slightly to the right when hovered
        self.rect.x += 5 if self.hovered else 0

b1 = Button(25, 600, 300, 100, (255,255,255), text="Play", hover_sound=pygame.mixer.Sound("data/select_002.ogg"))
buttons = [b1]

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
    // Calculate distance from center (assuming a centered vignette)
    vec2 center = vec2(0.5, 0.5);
    float distanceFromCenter = distance(uvs, center);

    // Adjust radii based on texture dimensions (assuming square texture)
    float textureSize = 1.0; // Replace with actual texture size if known
    float innerRadius = 0.2 * textureSize;
    float outerRadius = 0.8 * textureSize;

    // Calculate vignette strength
    float vignetteStrength = smoothstep(innerRadius, outerRadius, distanceFromCenter);

    // Apply vignette to texture color
    vec4 textureColor = texture(tex, uvs);
    f_color = vec4(textureColor.rgb * (1.0 - vignetteStrength), textureColor.a);
}
'''

shader = ShaderContext()


pygame.mixer.music.play(-1)

# Main game loop
running = True
while running:
    disp.fill((0,0,0))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                pygame.quit()


    disp.blit(img, (0,0))
    for i, cloud in enumerate(cloud_list):
        x_start[i]+=speeds[i]
        disp.blit(cloud, (x_start[i],y_vals[i]))
        if x_start[i] > 1200:
            x_start[i] = -400
    disp.blit(ts1, (150, 15))
    disp.blit(ts2, (75, 155))
    disp.blit(ts3, (15, 755))

    #for button in buttons:
        #button.update(pygame.mouse.get_pos(), disp)


    shader.update(disp)

    clock.tick(60)

