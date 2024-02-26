import pygame, sys

import pynamogui as pyn

# TODO: Make preset of floor, tile (autopopulate), wall, with dynamic size

pygame.init()
WIDTH, HEIGHT = 1200, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))

gui = pyn.gui
gui.set_screen(screen)
pyn.Page("config/page1")
pyn.Page("config/page2")
gui.current_page = "main"
gui.init_builder()

while True:
    screen.fill((0,0,0))
    pygame.display.set_caption(f"Level Editor v1.2: {gui.current_page}")  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gui.exit()

        elif event.type == pygame.MOUSEWHEEL:
            gui.handle_scroll(event)
           

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gui.exit()
            elif event.key == pygame.K_KP_MINUS or event.key == pygame.K_MINUS:
                gui.builder.change_brush_size(-1)
            elif event.key == pygame.K_KP_PLUS or event.key == pygame.K_PLUS:
                gui.builder.change_brush_size(1)

            gui.handle_button(event)


    gui.update()

    pygame.display.update()
    