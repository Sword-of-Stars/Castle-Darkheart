import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Tile dimensions
TILE_SIZE = 50

# Colors for visualization
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Function to get neighbors of a tile within grid bounds
def get_neighbors(grid, row, col):
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if 0 <= row + i < len(grid) and 0 <= col + j < len(grid[0]) and not (i == 0 and j == 0):
                neighbors.append((row + i, col + j))
    return neighbors

# Function to identify unique tile combinations
def identify_unique_tiles(grid):
    unique_tiles = set()
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            neighbors = get_neighbors(grid, row, col)
            cardinal_neighbors = [(i, j) for i, j in neighbors if abs(i - row) + abs(j - col) <= 1]
            diagonal_neighbors = [(i, j) for i, j in neighbors if abs(i - row) + abs(j - col) == 2]
            valid_diagonal_neighbors = [
                (i, j) for i, j in diagonal_neighbors
                if (row - 1, col) in cardinal_neighbors and (row, col - 1) in cardinal_neighbors or
                (row + 1, col) in cardinal_neighbors and (row, col + 1) in cardinal_neighbors
            ]
            neighbors = cardinal_neighbors + valid_diagonal_neighbors
            unique_tiles.add(tuple(grid[i][j] for i, j in neighbors))
    return unique_tiles

# Example grid (replace with your actual grid data)
grid = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Identify unique tiles
unique_tiles = identify_unique_tiles(grid)
print("Number of unique tile combinations:", len(unique_tiles))

# Visualize tiles (optional)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            color = BLACK if (row, col) == (1, 1) else WHITE  # Highlight center tile
            pygame.draw.rect(screen, color, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    pygame.display.update()

pygame.quit()
