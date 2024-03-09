import pygame, sys

#===== Pygame Initialization =====#
pygame.init()
pygame.mixer.init()

#===== Initial Imports =====#
from scripts.ui.menu import MenuScreen
from scripts.utils.game_loop import camera, clock, WIDTH, HEIGHT, mouse, main, reset
from scripts.ui.transition_screen import TransitionScreen

screen = pygame.display.set_mode((WIDTH, HEIGHT),  pygame.OPENGL | pygame.DOUBLEBUF)
menu = MenuScreen(WIDTH, HEIGHT, camera, clock, mouse, screen)
transition = TransitionScreen(screen, clock, camera)

state = "game"

#===== Main Loop =====#
while True:
    pygame.display.set_caption(str(state))
    check_game = True
    check_trans = True
    if state == "menu":
        state = menu.run(state)
        check_trans = False
    elif state == "game":
        state = main(state)
        check_game = False
    elif state == "transition":
        state = transition.run()
        check_trans = False


    if state == "game" and check_game: #chacking for changes
        pygame.mixer.music.stop()
        pygame.mixer.music.load("data/music/boss-1/Boss Theme Final.mp3")
        pygame.mixer.music.play(-1)
        reset()

    elif state == "transition" and check_trans: #chacking for changes
        transition = TransitionScreen(screen, clock, camera)

        camera.vignette = 0.8