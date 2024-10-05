import pygame
import sys
import random
from loop import loop, Object  # Import the game loop from the game.py file

# Game settings
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 30

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gravity simulator")

# Set up the clock for controlling the frame rate
clock = pygame.time.Clock()

# Main loop
def main():
    running = True

    state = initialise_state()
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Call the game loop function (from game.py)
        loop(screen, state)

        # Cap the frame rate at FPS (30 in this case)
        clock.tick(FPS)

    # Quit Pygame
    pygame.quit()
    sys.exit()

# Function to create the background surface with stars
def create_background(screen_width, screen_height, num_stars):
    background = pygame.Surface([screen_width, screen_height])
    background.fill((10, 10, 26))  # Fill with the dark space-like color

    # Draw stars on the background
    for _ in range(num_stars):
        x = random.randint(0, screen_width)
        y = random.randint(0, screen_height)
        size = random.randint(1, 3)

        # Determine color based on size
        color = (120, 120, size * 120/3, 0.5)

        pygame.draw.circle(background, color, (x, y), size)

    return background

def initialise_state():
    state = State()

    # set background
    state.background = create_background(SCREEN_WIDTH, SCREEN_HEIGHT, num_stars=100)
    state.objects = []

    # set objects
    state.objects.append(Object(mass=100, radius=20, color=(153, 102, 0), x=SCREEN_WIDTH/2, y=SCREEN_HEIGHT/2, velocity_x=0, velocity_y=0, stationary=True))
    state.objects.append(Object(mass=10, radius=10, color=(100, 100, 200), x=SCREEN_WIDTH/2 - 250, y=SCREEN_HEIGHT/2, velocity_x=0, velocity_y=-220, stationary=False))
    state.objects.append(Object(mass=0.1, radius=3, color=(100, 100, 200), x=SCREEN_WIDTH/2 - 290, y=SCREEN_HEIGHT/2, velocity_x=0, velocity_y=-390, stationary=False))
    # state.objects.append(Object(mass=50, radius=15, color=(153, 152, 0), x=SCREEN_WIDTH/2 + 100, y=SCREEN_HEIGHT/2, velocity_x=0, velocity_y=250, stationary=True))
    # state.objects.append(Object(mass=1, radius=7, color=(100, 100, 200), x=SCREEN_WIDTH/4, y=SCREEN_HEIGHT/2, velocity_x=0, velocity_y=-180))
    # state.objects.append(Object(mass=1, radius=7, color=(100, 100, 200), x=SCREEN_WIDTH/4 + 50, y=SCREEN_HEIGHT/2, velocity_x=0, velocity_y=-150))


    return state

class State():
    def __init__(self) -> None:
        self.background = None
        self.objects = []
        self.dragging_object = None  # To track if a drag is happening
        
if __name__ == "__main__":
    main()
