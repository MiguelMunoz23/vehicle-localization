#!/usr/bin/python3
"""
vehicle-localization.py

This Python script implements the equations for an autonomous car and uses pygame to visualize an animation.

Author: Miguel Angel Muñoz Rizo

Institution: Universidad de Monterrey
Subject: Advanced Robotics
Lecturer: Dr. Andrés Hernández Gutiérrez

Date of creation: 28 August 2022
"""

import argparse
from math import sin, cos, atan2, tan, pi

# Import useful libraries
import pygame
from numpy import deg2rad, rad2deg

# Initialize pygame and constants
pygame.init()
FONT = pygame.font.Font(None, 20)

# Create a window
WIDTH, HEIGHT = 600, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ackerman Steering Simulator | Advanced Robotics")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SKY_BLUE = (0, 170, 228)
GREEN = (0, 255, 0)

# Define speed limits
UPPER_SPEED_LIMIT = 300
LOWER_SPEED_LIMIT = 0


class Car:
    """
    This class is used to define the parameters related to the car. Here the Ackermann dynamic equations are implemented
    and the car is drawn in the window.
    """
    ANGLE_STEP = 1.2  # [°]
    SPEED_STEP = 10  # [km/h]
    METERS_PER_PIXEL = 2  # 1 px = 2 mts

    def __init__(self, vehicle_speed, lf, lb, x0, y0, psi0, df0, dt):
        """
        This is the constructor. These variables come from the arguments specified in the terminal.
        :param vehicle_speed (int): Speed of the vehicle [km/h].
        :param lf (float): Distance from vehicle's center of mass to the front wheel axle [m].
        :param lb (float): Distance from vehicle's center of mass to the back wheel axle [m].
        :param x0 (float): x-coordinate for the initial position [m].
        :param y0 (float): y-coordinate for the initial position [m].
        :param psi0 (float): Initial Heading Angle [°].
        :param df0 (float): Initial front wheel rotation angle [°].
        :param dt (float): Sampling time interval [sec].
        """
        self.vel, self.vel_k_1 = vehicle_speed, 0  # 1 = 100 [km/h]
        self.lf = lf
        self.lb = lb
        self.x_k, self.x_k_1 = x0, x0
        self.y_k, self.y_k_1 = y0, y0
        self.psi, self.psi_k_1 = psi0, psi0
        self.delta_k, self.delta_k_1 = df0, df0
        self.delta_t = dt

        self.image = None
        self.width = 40
        self.height = 20
        self.x_pos = 0
        self.y_pos = 0
        self.past_positions = []
        self.beta_k_1 = 0

    def draw(self, window):
        """
        This method is used to draw all the car-related features.
        :param window: Pygame window object.
        :return: None
        """
        # Set the position of the car with respect to the center of the window
        self.x_pos = WIDTH // 2 + self.x_k / self.METERS_PER_PIXEL
        self.y_pos = HEIGHT // 2 + self.y_k * -1 / self.METERS_PER_PIXEL

        # Rotate the image with respect to the angle
        self.image = pygame.transform.rotate(
            pygame.transform.scale(pygame.image.load('car.png'), (self.width, self.height)), rad2deg(self.psi))

        # Leaving trail (save all past positions)
        self.past_positions.append([self.x_pos, self.y_pos])
        for point in self.past_positions:
            pygame.draw.circle(window, SKY_BLUE, point, 2)
            
        # Draw circle in the center of the screen just for visualization
        pygame.draw.circle(window, WHITE, (WIDTH//2, HEIGHT//2), 5)

        # Display processed car image in the correct position and rotate with respect to the center of the image
        window.blit(self.image, self.image.get_rect(center=(self.x_pos, self.y_pos)))
        return None

    def move(self, up=None, up_left=None, up_right=None, down=None, down_left=None, down_right=None, speed_up=None,
             speed_down=None, not_moving=None):
        """
        This method determines the direction and velocity in which the car is moving.
        :param up: Determines if the car is moving forwards.
        :param up_left: Determines if the car is moving forwards left with respect to the vehicle frame.
        :param up_right: Determines if the car is moving forwards right with respect to the vehicle frame.
        :param down: Determines if the car is moving backwards.
        :param down_left: Determines if the car is moving backwards left with respect to the vehicle frame.
        :param down_right: Determines if the car is moving backwards right with respect to the vehicle frame.
        :param speed_up: Determines if the velocity increases.
        :param speed_down: Determines if the velocity decreases.
        :param not_moving: Determines if the car is not moving.
        :return: 
        """
        self.vel_k_1 = self.vel
        # Check every condition and move the car accordingly
        if up:  # Forwards
            self.delta_k = 0
        if up_left:  # Forwards left
            self.delta_k = self.ANGLE_STEP * -1
        if up_right:  # Forwards right
            self.delta_k = self.ANGLE_STEP
        if down:  # Backwards
            self.delta_k = 0
            self.vel_k_1 *= -1
        if down_left:  # Backwards left
            self.delta_k = self.ANGLE_STEP
            self.vel_k_1 *= -1
        if down_right:  # Backwards right
            self.delta_k = self.ANGLE_STEP * -1
            self.vel_k_1 *= -1
        if speed_up:  # Velocity increases
            self.vel += self.SPEED_STEP
        if speed_down:  # Velocity increases
            self.vel -= self.SPEED_STEP
        if not_moving:  # Vehicle not moving
            self.vel_k_1 = 0
        return None

    def print_parameters(self, window):
        """
        This method prints the car parameters in the top left corner of the window.
        :param window: Pygame window object.
        :return: None.
        """
        # Create list with the text to display
        texts = ["CONFIG. PARAMS",
                 f"Speed: {self.vel:.2f} km/h",
                 f"\u0394T: {self.delta_t} s",
                 f"\u0394f increment: {self.ANGLE_STEP} °",
                 f"Lb: {self.lb} m",
                 f"Lf: {self.lf} m"]
        text_x, text_y = 20, 20
        i = 0
        # Display each item in the texts list
        for text in texts:
            text_rendered = FONT.render(text, True, WHITE)
            window.blit(text_rendered, (text_x, text_y + i))
            # These lines are used to define the text location automatically
            if i == 0:
                i += 20
            i += 15
        return None

    def apply_equations(self):
        """
        This method applies the Ackermann dynamic equations and also prints the beta, x, y and psi values in the
        terminal.
        :return: None.
        """
        # Save previous values in the k-1 variables
        self.delta_k_1 = self.delta_k
        self.x_k_1 = self.x_k
        self.y_k_1 = self.y_k
        self.psi_k_1 = self.psi

        # Ackermann dynamic equations
        self.beta_k_1 = atan2((self.lb * tan(deg2rad(self.delta_k_1))), (self.lf + self.lb))
        self.x_k = self.x_k_1 + self.vel_k_1/3.6 * self.delta_t * cos(self.psi_k_1 + self.beta_k_1)
        self.y_k = self.y_k_1 + self.vel_k_1/3.6 * self.delta_t * sin(self.psi_k_1 + self.beta_k_1)
        self.psi = (self.psi_k_1 + self.vel_k_1/3.6 * self.delta_t * cos(self.beta_k_1) * tan(
            deg2rad(self.delta_k_1)) / (self.lf + self.lb)) % (2 * pi)

        # Print the information in the terminal
        print(f"Beta: {rad2deg(self.beta_k_1):.3f}°, x: {self.x_k:.3f} m, y: {self.y_k:.3f} m, "
              f"heading_angle: {rad2deg(self.psi):.3f}°")
        return None

    def print_position(self, window):
        """
        This method prints the current x, y and psi car values that follow the car in the pygame window.
        :param window: Pygame window object.
        :return: None
        """
        self.apply_equations()
        # Print the current x, y and psi of the vehicle after applying the equations
        position_str = f"({self.x_k:.3f} m, {self.y_k:.3f} m, {(rad2deg(self.psi)):.3f} °)"
        position_rendered = FONT.render(position_str, True, GREEN)
        window.blit(position_rendered, (self.x_pos + 15, self.y_pos + 15))
        return None


def draw(window, car):
    """
    This function is used to update the pygame window with the background and all the car-related features.
    :param window: Pygame window object.
    :param car: Instance of the class Car.
    :return: None
    """
    WINDOW.fill(BLACK)
    car.draw(window)
    car.print_parameters(window)
    car.print_position(window)
    pygame.display.update()
    return None


def handle_movement(car, keys):
    """
    This function is used to handle the car movement with several conditionals that check which keys are being pressed
    by the user.
    :param car: Instance of the class Car.
    :param keys: A list containing all the keys that are being pressed.
    :return: None
    """
    # Check which keys are being pressed
    moving = False
    if keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
        moving = True
    if keys[pygame.K_UP] and not (keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
        car.move(up=True)
    if keys[pygame.K_UP] and keys[pygame.K_LEFT] and not (keys[pygame.K_DOWN] or keys[pygame.K_RIGHT]):
        car.move(up_left=True)
    if keys[pygame.K_UP] and keys[pygame.K_RIGHT] and not (keys[pygame.K_DOWN] or keys[pygame.K_LEFT]):
        car.move(up_right=True)
    if keys[pygame.K_DOWN] and not (keys[pygame.K_UP] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
        car.move(down=True)
    if keys[pygame.K_DOWN] and keys[pygame.K_LEFT] and not (keys[pygame.K_UP] or keys[pygame.K_RIGHT]):
        car.move(down_left=True)
    if keys[pygame.K_DOWN] and keys[pygame.K_RIGHT] and not (keys[pygame.K_UP] or keys[pygame.K_LEFT]):
        car.move(down_right=True)
    if keys[pygame.K_f] and car.vel < UPPER_SPEED_LIMIT and moving:
        car.move(speed_up=True)
    if keys[pygame.K_s] and car.vel > LOWER_SPEED_LIMIT and moving:
        car.move(speed_down=True)
    if not moving:
        car.move(not_moving=True)
    return None


def main(vehicle_speed, lf, lb, x0, y0, psi0, df0, dt):
    """
    This function is the main loop of the simulation. Here the program is being limited to run every 1/dt seconds.
    :param vehicle_speed: Speed of the vehicle [km/h]. (float)
    :param lf: Distance from vehicle's center of mass to the front wheel axle [m]. (float)
    :param lb: Distance from vehicle's center of mass to the back wheel axle [m]. (float)
    :param x0: x-coordinate for the initial position [m]. (float)
    :param y0: y-coordinate for the initial position [m]. (float)
    :param psi0: Initial Heading Angle [°]. (float)
    :param df0: Initial front wheel rotation angle [°]. (float)
    :param dt: Sampling time interval [sec]. (float)
    :return: None
    """
    run = True
    clock = pygame.time.Clock()
    # Define the maximum FPS for the simulation
    fps = 1 / dt

    # Create instance of the class Car with the parameters that the user introduced in the arguments
    car = Car(vehicle_speed, lf, lb, x0, y0, psi0, df0, dt)
    while run:
        clock.tick(fps)
        # Draw in the window
        draw(WINDOW, car)
        # Check pressed keys and handle the movement
        keys = pygame.key.get_pressed()
        handle_movement(car, keys)
        # Check if the user clicks the 'X' button in the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
    # If simulation closed, quit pygame
    pygame.quit()


if __name__ == '__main__':
    # Parsing the arguments introduced by the user
    parser = argparse.ArgumentParser(description="Give parameters for the car")
    parser.add_argument('--vehicle_speed', type=int, help="Speed of the vehicle [km/h]")
    parser.add_argument('--lf', type=float, help="Distance from vehicle's center of mass to the front wheel axle [m]")
    parser.add_argument('--lb', type=float, help="Distance from vehicle's center of mass to the back wheel axle [m]")
    parser.add_argument('--x0', type=float, help="x-coordinate for the initial position [m]")
    parser.add_argument('--y0', type=float, help="y-coordinate for the initial position [m]")
    parser.add_argument('--psi0', type=float, help="Initial Heading Angle [°]")
    parser.add_argument('--df0', type=float, help="Initial front wheel rotation angle [°]")
    parser.add_argument('--dt', type=float, help="Sampling time interval [sec]")
    args = parser.parse_args()
    # Call the main function and send the user-defined parameters
    main(args.vehicle_speed, args.lf, args.lb, args.x0, args.y0, deg2rad(args.psi0), deg2rad(args.df0), args.dt)
