import math
import pygame

def circle_intersection(c1, r1, c2, r2):
  """
  Calculates the intersection points between two circles.

  Args:
    c1: Center coordinates of circle 1 (x, y).
    r1: Radius of circle 1.
    c2: Center coordinates of circle 2 (x, y).
    r2: Radius of circle 2.

  Returns:
    A list of two intersection points as tuples [(x1, y1), (x2, y2)].
  """
  dx, dy = c2[0] - c1[0], c2[1] - c1[1]
  distance = math.sqrt(dx**2 + dy**2)
  if distance > r1 + r2 or distance < abs(r1 - r2):
    return []  # No intersection
  sum_radii = r1 + r2
  diff_radii = abs(r1 - r2)
  a = (sum_radii**2 - distance**2) / (2 * distance)
  h = math.sqrt(max(0,sum_radii**2 - a**2))
  x2 = c1[0] + dx * a / distance
  y2 = c1[1] + dy * a / distance
  x1 = x2 + dx * h / distance
  y1 = y2 + dy * h / distance
  return [(x1, y1), (x2, y2)]

def draw_bitangents(screen, c1, r1, c2, r2, color):
  """
  Draws lines representing the internal bitangents between two circles.

  Args:
    screen: The Pygame display surface.
    c1: Center coordinates of circle 1 (x, y).
    r1: Radius of circle 1.
    c2: Center coordinates of circle 2 (x, y).
    r2: Radius of circle 2.
    color: The color of the lines (RGB tuple).
  """
  intersections = circle_intersection(c1, r1, c2, r2)
  if intersections:
    pygame.draw.circle(screen, (255, 0, 0), c1, int(r1), 2)
    pygame.draw.circle(screen, (0, 255, 0), c2, int(r2), 2)
    for point in intersections:
      pygame.draw.line(screen, color, c1, point, 2)

# Pygame initialization
pygame.init()
screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Internal Bitangents")

# Circle parameters
c1 = (screen_width // 2, screen_height // 2)
r1 = 100
c2 = (c1[0] + 150, c1[1])
r2 = 80

# Main loop
running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  c2 = pygame.mouse.get_pos()

  screen.fill((0, 0, 0))
  draw_bitangents(screen, c1, r1, c2, r2, (255, 255, 255))
  pygame.display.flip()

pygame.quit()
