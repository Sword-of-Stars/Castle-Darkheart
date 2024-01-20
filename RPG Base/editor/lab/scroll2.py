import pygame

pygame.init()

# define the screen size and scroll speed
screen_width = 800
screen_height = 600
scroll_speed = 10

# create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Image Scrolling")

# create a list of images to scroll
images = [
    pygame.image.load("editor/lab/load.png") for i in range(5)]

# calculate the total height of all the images
total_height = sum([img.get_height() for img in images])

# create a rectangle to represent the visible portion of the screen
viewport = pygame.Rect(0, 0, screen_width, screen_height)

# create a variable to represent the current scroll position
scroll_pos = 0

# main game loop
running = True
while running:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # get the current keyboard state
    keys = pygame.key.get_pressed()

    # scroll up if the up arrow key is pressed
    if keys[pygame.K_UP]:
        scroll_pos = max(0, scroll_pos - scroll_speed)

    # scroll down if the down arrow key is pressed
    if keys[pygame.K_DOWN]:
        scroll_pos = min(total_height - viewport.height, scroll_pos + scroll_speed)

    # clear the screen
    screen.fill((255, 255, 255))

    # draw the visible portion of the images
    y = -scroll_pos
    for img in images:
        img_rect = img.get_rect()
        img_rect.y = y
        if img_rect.colliderect(viewport):
            
            img_clip = img.subsurface(viewport.clip(img_rect))
            screen.blit(img_clip, img_rect.move(0, scroll_pos))
        y += img.get_height()

    # update the display
    pygame.display.flip()

# quit pygame
pygame.quit()
