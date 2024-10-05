import pygame
import random
import math

ACCELERATION_SCALE = 100000
SOFTENING_FACTOR = 2

class Object():
    def __init__(self, mass, radius, color, x, y, velocity_x, velocity_y, stationary=False) -> None:
        self.mass = mass
        self.radius = radius
        self.color = color
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.stationary = stationary

def show_objects(screen, objects):
    for object in objects:
        pygame.draw.circle(screen, object.color, (object.x, object.y), object.radius)

    pass


import math

# Helper function to calculate force and acceleration between two objects
def compute_acceleration(object, object_other):
    dx = object_other.x - object.x
    dy = object_other.y - object.y
    distance = math.sqrt(dx**2 + dy**2 + SOFTENING_FACTOR**2)
    
    if distance == 0:  # Avoid division by zero
        return 0, 0
    
    # Gravitational force magnitude (ignoring constant)
    force = ACCELERATION_SCALE * (object.mass * object_other.mass) / distance**2
    force_x = force * (dx / distance)
    force_y = force * (dy / distance)
    
    # Calculate acceleration
    acceleration_x = force_x / object.mass
    acceleration_y = force_y / object.mass
    
    return acceleration_x, acceleration_y

def runge_kutta_step(object, objects, delta_t):
    # Initialize total accelerations
    total_acc_x = 0
    total_acc_y = 0
    
    for object_other in objects:
        if object == object_other:
            continue
        acc_x, acc_y = compute_acceleration(object, object_other)
        total_acc_x += acc_x
        total_acc_y += acc_y
    
    # RK4 for velocity
    k1_vx = total_acc_x * delta_t
    k1_vy = total_acc_y * delta_t
    
    k2_vx = (total_acc_x + k1_vx / 2) * delta_t
    k2_vy = (total_acc_y + k1_vy / 2) * delta_t
    
    k3_vx = (total_acc_x + k2_vx / 2) * delta_t
    k3_vy = (total_acc_y + k2_vy / 2) * delta_t
    
    k4_vx = (total_acc_x + k3_vx) * delta_t
    k4_vy = (total_acc_y + k3_vy) * delta_t
    
    # Update velocity
    object.velocity_x += (k1_vx + 2*k2_vx + 2*k3_vx + k4_vx) / 6
    object.velocity_y += (k1_vy + 2*k2_vy + 2*k3_vy + k4_vy) / 6
    
    # RK4 for position
    k1_px = object.velocity_x * delta_t
    k1_py = object.velocity_y * delta_t
    
    k2_px = (object.velocity_x + k1_px / 2) * delta_t
    k2_py = (object.velocity_y + k1_py / 2) * delta_t
    
    k3_px = (object.velocity_x + k2_px / 2) * delta_t
    k3_py = (object.velocity_y + k2_py / 2) * delta_t
    
    k4_px = (object.velocity_x + k3_px) * delta_t
    k4_py = (object.velocity_y + k3_py) * delta_t
    
    # Update position
    object.x += (k1_px + 2*k2_px + 2*k3_px + k4_px) / 6
    object.y += (k1_py + 2*k2_py + 2*k3_py + k4_py) / 6

# Main function for updating positions using RK4
def calculate_new_object_positions(objects, delta_t=1/60):
    for object in objects:
        if object.stationary:
            continue
        runge_kutta_step(object, objects, delta_t)


def calculate_gravitational_pull(x, y, objects, softening_factor=0.01):
    """Calculate the gravitational acceleration at point (x, y) due to all objects."""
    total_acc_x = 0
    total_acc_y = 0
    
    for obj in objects:
        dx = obj.x - x
        dy = obj.y - y
        distance = math.sqrt(dx**2 + dy**2)  # Softening factor to avoid singularity
        
        # Gravitational acceleration (ignoring the constant G)
        acc = 50*obj.mass / (distance**2)
        total_acc_x += acc * (dx / distance)
        total_acc_y += acc * (dy / distance)
    
    return total_acc_x, total_acc_y

def draw_gravitational_map(screen, objects, grid_spacing=15):
    """Draws the gravitational map with lines showing the direction and magnitude of gravity."""
    screen_width, screen_height = screen.get_size()
    
    # Loop over grid points spaced by `grid_spacing`
    for x in range(0, screen_width, grid_spacing):
        for y in range(0, screen_height, grid_spacing):
            acc_x, acc_y = calculate_gravitational_pull(x, y, objects)
            
            # Calculate the magnitude of the acceleration
            magnitude = math.sqrt(acc_x**2 + acc_y**2)
            
            if magnitude == 0:
                continue  # Skip points with no pull
            
            # Normalize the acceleration vector
            norm_acc_x = acc_x / magnitude
            norm_acc_y = acc_y / magnitude
            
            # Scale the line length based on the magnitude (scaling factor for visibility)
            line_length = min(magnitude * 10, grid_spacing) + 5
            
            # Determine the endpoint of the line (starting point is the grid point (x, y))
            end_x = x + norm_acc_x * line_length
            end_y = y + norm_acc_y * line_length
            
            # Draw the line representing the gravitational force direction and magnitude
            pygame.draw.line(screen, (100, 100, 100), (x, y), (end_x, end_y), 1)

# Constants for new objects
NEW_OBJECT_MASS = 1
NEW_OBJECT_RADIUS = 7

# Function to handle mouse dragging and create new objects
def handle_mouse_events(state):
    mouse_pressed = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    
    if mouse_pressed[0]:  # If left mouse button is pressed
        if state.dragging_object is None:
            # Start dragging: record the starting position
            state.dragging_object = {
                "start_pos": mouse_pos,
                "current_pos": mouse_pos
            }
        else:
            # Update the current position while dragging
            state.dragging_object["current_pos"] = mouse_pos
    else:
        # If the mouse is released and we were dragging
        if state.dragging_object is not None:
            start_pos = state.dragging_object["start_pos"]
            end_pos = state.dragging_object["current_pos"]
            
            # Calculate the velocity based on drag distance and a constant factor
            velocity_x = (start_pos[0] - end_pos[0]) * 0.1
            velocity_y = (start_pos[1] - end_pos[1]) * 0.1
            
            # Create a new object with random color and calculated velocity
            new_object = Object(
                mass=NEW_OBJECT_MASS,
                radius=NEW_OBJECT_RADIUS,
                color=(random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)),
                x=start_pos[0],
                y=start_pos[1],
                velocity_x=velocity_x*25,
                velocity_y=velocity_y*25
            )
            
            state.objects.append(new_object)
            
            # Stop dragging
            state.dragging_object = None

def draw_drag_line(screen, state):
    """Draws a line showing the drag direction and distance."""
    if state.dragging_object:
        start_pos = state.dragging_object["start_pos"]
        current_pos = state.dragging_object["current_pos"]
        pygame.draw.line(screen, (255, 255, 255), start_pos, current_pos, 2)

# Loop function
def loop(screen, state):
    screen.blit(state.background, (0, 0))

    # screen_width, screen_height = screen.get_size()

    handle_mouse_events(state)

    draw_drag_line(screen, state)

    calculate_new_object_positions(state.objects)

    draw_gravitational_map(screen, state.objects)

    show_objects(screen, state.objects)


    # screen.fill((20, 20, 36))  # Fill the screen with white

    # Draw a red rectangle as an example
    # SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    # pygame.draw.rect(screen, (255, 0, 0), (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 50, 100, 100))

    # Update the display
    pygame.display.flip()

