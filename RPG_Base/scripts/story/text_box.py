import pygame, sys

from scripts.utils.core_functions import prep_image

font_lg = pygame.font.Font("data/fonts/oldenglish.ttf", 40)
font_sm = pygame.font.Font("data/fonts/oldenglish.ttf", 32)

def split_and_rejoin(text):
    """
    Splits a string for every newline character, and rejoins the strings in pairs,
    with newline characters in between the new pairs.

    Args:
    text: The string to split and rejoin.

    Returns:
    The rejoined string.
    """

    # Split the string into lines.
    lines = text.splitlines()

 # If there are less than two lines, return the original text.
    if len(lines) < 2:
        return [text]

    # Rejoin the lines in pairs, with newline characters in between.
    result = []
    for i in range(0, len(lines), 2):
        pair = lines[i] + "\n"
        if i + 1 < len(lines):
            pair += lines[i + 1]
        result.append(pair)

    return result



class TextBox():
    def __init__(self, character, msg):
        self.pos = [235,575] # read from config, need to make a centralized config file

        self.character = character
        self.character_text = font_lg.render(character, False, (255,255,255))
        self.text_pos = [400,600]
        self.overlay = prep_image(pygame.image.load("data/portrait_overlay.png"), 3, colorkey=(0,0,0))
        self.img = pygame.transform.scale_by(pygame.image.load("data/book.png"), 1.5).convert_alpha()

        self.all_msgs = split_and_rejoin(msg) # paired messages by 2s
        self.current_msg = 0
        self.num_msg = len(self.all_msgs)
        self.msg = self.all_msgs[0]
        self.msg_len = len(self.msg)
        self.msg_pointer = 0
        self.msg_pos = [self.text_pos[0], self.text_pos[1]+50]
        self.msg_text = font_sm.render(msg, False, (255,255,255))

        self.reveal_speed = 0.5

        self.msg_finished = False
        self.all_finished = False


    def update_msg(self):
        self.msg_text = font_sm.render(self.msg[:int(self.msg_pointer)], False, (255,255,255))
        self.msg_pointer += self.reveal_speed

        if self.msg_pointer >= self.msg_len:
            self.msg_finished = True

    def skip(self): # skip to end of sequence
        self.msg_pointer = self.msg_len

    def next(self): #progress to the next text box
        if not self.msg_finished:
            self.skip()
        else:
            if self.current_msg < self.num_msg-1:
                self.current_msg += 1

                self.msg = self.all_msgs[self.current_msg]
                self.msg_len = len(self.msg)
                self.msg_finished = False

                self.msg_pointer = 0
            else:
                self.all_finished = True

    def reset(self):
        self.msg_pointer = 0
        self.current_msg = 0
        self.msg = self.all_msgs[0]

        self.msg_finished = False
        self.all_finished = False

    def update(self, camera):
        self.update_msg()
        camera.ui_surf.blit(self.character_text, self.text_pos)
        camera.ui_surf.blit(self.msg_text, self.msg_pos)

        camera.ui_surf.blit(self.img, self.pos)
        camera.ui_surf.blit(self.overlay, self.pos)

    