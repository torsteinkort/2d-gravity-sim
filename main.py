import pygame
import sys
import random
from loop import loop, Object

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 30

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gravity simulator")

clock = pygame.time.Clock()

def main():
    running = True

    state = initialise_state()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        loop(screen, state)

        clock.tick(FPS)

    pygame.quit()
    sys.exit()

def create_background(screen_width, screen_height, num_stars):
    background = pygame.Surface([screen_width, screen_height])
    background.fill((10, 10, 26))

    for _ in range(num_stars):
        # draw stars
        x = random.randint(0, screen_width)
        y = random.randint(0, screen_height)
        size = random.randint(1, 3)

        color = (120, 120, size * 120/3, 0.5)

        pygame.draw.circle(background, color, (x, y), size)

    return background

def initialise_state():
    state = State()

    # set background
    state.background = create_background(SCREEN_WIDTH, SCREEN_HEIGHT, num_stars=100)
    state.objects = []

    # set objects
    state.objects.append(Object(mass=100, radius=35, color=(153, 102, 0), x=SCREEN_WIDTH/2, y=SCREEN_HEIGHT/2, velocity_x=0, velocity_y=0, stationary=True))
    state.objects.append(Object(mass=10, radius=15, color=(100, 100, 200), x=SCREEN_WIDTH/2 - 250, y=SCREEN_HEIGHT/2, velocity_x=0, velocity_y=-210, stationary=False))
    state.objects.append(Object(mass=0.1, radius=5, color=(100, 100, 200), x=SCREEN_WIDTH/2 - 290, y=SCREEN_HEIGHT/2, velocity_x=0, velocity_y=-370, stationary=False))
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
