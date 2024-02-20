import pygame
import os

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("File Browser")

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# Set up fonts
font = pygame.font.Font(None, 28)

# Set up file browser parameters
current_path = os.getcwd()
selected_file = None

# Function to list files and directories in the current path
def list_files():
    file_list = []
    for item in os.listdir(current_path):
        file_list.append(item)
    return file_list

# Function to handle file selection
def select_file(file_name):
    global selected_file
    selected_file = file_name
    print("Selected file:", selected_file)

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Get the mouse position
                mouse_pos = pygame.mouse.get_pos()
                # Calculate the clicked row index
                row_index = mouse_pos[1] // 30
                # Get the file list
                files = list_files()
                # Check if the row index is valid
                if row_index < len(files):
                    file_name = files[row_index]
                    # Check if it's a directory
                    if os.path.isdir(os.path.join(current_path, file_name)):
                        # Update the current path
                        current_path = os.path.join(current_path, file_name)
                    else:
                        # Select the file
                        select_file(file_name)

    # Clear the screen
    screen.fill(WHITE)

    # Draw the file list
    files = list_files()
    for i, file_name in enumerate(files):
        # Set the text color based on selection
        text_color = BLACK if file_name != selected_file else GRAY
        # Render the file name
        text = font.render(file_name, True, text_color)
        # Draw the file name on the screen
        screen.blit(text, (20, 30 * i + 20))

    # Update the display
    pygame.display.flip()

# Quit the program
pygame.quit()
