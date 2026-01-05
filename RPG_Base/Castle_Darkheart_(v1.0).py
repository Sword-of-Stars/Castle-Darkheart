import pygame, sys

#===== Pygame Initialization =====#
pygame.init()
pygame.mixer.init()

#===== Initial Imports =====#
from scripts.ui.menu import MenuScreen
from scripts.utils.game_loop import camera, clock, WIDTH, HEIGHT, mouse, main, reset
from scripts.ui.transition_screen import TransitionScreen
from scripts.ui.credits import Credits

screen = pygame.display.set_mode((WIDTH, HEIGHT),  pygame.OPENGL | pygame.DOUBLEBUF)
menu = MenuScreen(WIDTH, HEIGHT, camera, clock, mouse, screen)
transition = TransitionScreen(screen, clock, camera)
cred = Credits(WIDTH, HEIGHT, camera, clock, mouse, screen)

pygame.display.set_caption("Castle Darkheart")

state = "menu"

if state == "menu":
    menu.start()

elif state == "game":
    reset()

elif state == "credits":
    cred.start()

#===== Main Loop =====#
while True:
    pygame.display.set_caption(str(state))
    check_game = True
    check_trans = True
    check_cred = True
    
    if state == "menu":
        state = menu.run(state)
        check_trans = False
    elif state == "game":
        state, track = main(state)
        check_game = False
    elif state == "transition":
        state = transition.run()
        check_trans = False

    elif state == "credits":
        cred.run()
        check_cred = False


    if state == "game" and check_game: 
        reset()

    if state == "transition" and check_trans:
        transition = TransitionScreen(screen, clock, camera)

        camera.vignette = 0.8

    elif state == "menu" and check_trans:
        menu.start()

    elif state == "credits" and check_cred:
        cred.start()