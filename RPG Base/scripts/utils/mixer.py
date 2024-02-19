import pygame, sys

class Mixer():
    # I envision this class will play any music or extra sound effects required, not tied to specific entities
    # Plays background music 
    def __init__(self):
        pass
    def play_bg(self):
        pygame.mixer.music.load('data/music/main-1/dgv_03.mp3')
        pygame.mixer.music.play(-1)