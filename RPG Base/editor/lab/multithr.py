import pygame
import easygui
import threading

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame Window")

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Function to run Pygame in a separate thread
def run_pygame():
    # Game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill(WHITE)

        # Update the display
        pygame.display.flip()

    # Quit the program
    pygame.quit()

# Function to run EasyGUI in a separate thread
def run_easygui():
    # Open an EasyGUI window
    easygui.msgbox("This is an EasyGUI window.")

# Create threads for Pygame and EasyGUI windows
pygame_thread = threading.Thread(target=run_pygame)
easygui_thread = threading.Thread(target=run_easygui)

# Start the threads
pygame_thread.start()
easygui_thread.start()

# Wait for both threads to finish
pygame_thread.join()
easygui_thread.join()
