import pygame, sys

def handle_events(player):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                player.pressed["right"] = True
                player.most_recent_press["horizontal"] = "right"
            elif event.key == pygame.K_a:
                player.pressed["left"] = True
                player.most_recent_press["horizontal"] = "left"
            elif event.key == pygame.K_w:
                player.pressed["up"] = True
                player.most_recent_press["vertical"] = "up"
            elif event.key == pygame.K_s:
                player.pressed["down"] = True
                player.most_recent_press["vertical"] = "down"
            elif event.key == pygame.K_SPACE:
                player.pressed["space"] = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                player.pressed["right"] = False
                player.most_recent_press["horizontal"] = ""
            elif event.key == pygame.K_a:
                player.pressed["left"] = False
                player.most_recent_press["horizontal"] = ""
            elif event.key == pygame.K_w:
                player.pressed["up"] = False
                player.most_recent_press["vertical"] = ""
            elif event.key == pygame.K_s:
                player.pressed["down"] = False
                player.most_recent_press["vertical"] = ""
            elif event.key == pygame.K_SPACE:
                player.pressed["space"] = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                player.sword.swing()
