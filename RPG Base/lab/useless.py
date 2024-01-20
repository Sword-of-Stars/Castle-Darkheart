# Functions #
import pygame

font = pygame.font.SysFont('ErasITC', 20)
WIDTH, HEIGHT = 800,600
screen = pygame.display.set_mode((WIDTH, HEIGHT))


def render_presses(pressed):
    left = font.render(str(pressed["left"]), False, (0,255,0))
    right = font.render(str(pressed["right"]), False, (0,255,0))
    up = font.render(str(pressed["up"]), False, (0,255,0))
    down = font.render(str(pressed["down"]), False, (0,255,0))

    screen.blit(left, (0,0))
    screen.blit(right, (0,20))
    screen.blit(up, (0,40))
    screen.blit(down, (0,60))
