import pygame
import math

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()

# Set the width and height of the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Inverse Kinematics Visualization")

# Set up the clock
clock = pygame.time.Clock()

# Set up the robot arm parameters
arm_length = 100
num_joints = 3
joint_radius = 10
target_radius = 10
joint_speed = 0.1

# Initialize joint angles
joint_angles = [0] * num_joints

# Initialize target position
target_position = [screen_width // 2, screen_height // 2]

running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(WHITE)

    # Get mouse position
    mouse_pos = pygame.mouse.get_pos()
    target_position[0] = mouse_pos[0]
    target_position[1] = mouse_pos[1]

    # Perform inverse kinematics
    joint_positions = []
    x = screen_width // 2
    y = screen_height // 2
    for i in range(num_joints):
        angle = joint_angles[i]
        end_x = x + arm_length * math.cos(angle)
        end_y = y + arm_length * math.sin(angle)
        pygame.draw.line(screen, BLACK, (x, y), (end_x, end_y), 5)
        joint_positions.append((x, y))
        x = end_x
        y = end_y

    # Draw the target
    pygame.draw.circle(screen, RED, target_position, target_radius)

    # Update the screen
    pygame.display.flip()

    # Control joint speed
    for i in range(num_joints):
        current_angle = joint_angles[i]
        target_angle = math.atan2(target_position[1] - joint_positions[i][1], target_position[0] - joint_positions[i][0])
        difference = target_angle - current_angle

        if abs(difference) > joint_speed:
            if difference > 0:
                joint_angles[i] += joint_speed
            else:
                joint_angles[i] -= joint_speed

    # Limit the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
