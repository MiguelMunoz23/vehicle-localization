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
FPS = 120
FONT = pygame.font.Font(None, 20)

# Create a window
WIDTH, HEIGHT = 800, 800
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
    ANGLE_STEP = 1.2  # [°]
    SPEED_STEP = 2  # [km/h]
    METERS_PER_PIXEL = 2  # 1 px = 2 mts

    def __init__(self, vehicle_speed, lf, lb, x0, y0, phi0, df0, dt):
        self.vel, self.vel_k_1 = vehicle_speed, 0  # 1 = 100 [km/h]
        self.lf = lf
        self.lb = lb
        self.x_k, self.x_k_1 = x0, x0
        self.y_k, self.y_k_1 = y0, y0
        self.phi, self.phi_k_1 = phi0, phi0
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
        self.x_pos = WIDTH // 2 + self.x_k / self.METERS_PER_PIXEL
        self.y_pos = HEIGHT // 2 + self.y_k * -1 / self.METERS_PER_PIXEL

        # Rotate the image with respect to the angle
        self.image = pygame.transform.rotate(
            pygame.transform.scale(pygame.image.load('car.png'), (self.width, self.height)), rad2deg(self.phi))

        # Leaving trail
        self.past_positions.append([self.x_pos, self.y_pos])
        for point in self.past_positions:
            pygame.draw.circle(window, SKY_BLUE, point, 2)
        # Draw center of the screen
        pygame.draw.circle(window, WHITE, (WIDTH//2, HEIGHT//2), 5)

        # Display car image in the center of the screen and add the x and y coordinate
        window.blit(self.image, self.image.get_rect(center=(self.x_pos, self.y_pos)))

    def move(self, up=None, up_left=None, up_right=None, down=None, down_left=None, down_right=None, speed_up=None,
             speed_down=None, not_moving=None):
        self.vel_k_1 = self.vel
        # Check every condition and move the car accordingly
        if up:  # Forward
            self.delta_k = 0
        if up_left:  # Forward left
            self.delta_k = self.ANGLE_STEP
        if up_right:  # Forward right
            self.delta_k = self.ANGLE_STEP * -1
        if down:  # Backwards
            self.delta_k = 0
            self.vel_k_1 *= -1
        if down_left:  # Backwards left
            self.delta_k = self.ANGLE_STEP * -1
            self.vel_k_1 *= -1
        if down_right:  # Backwards right
            self.delta_k = self.ANGLE_STEP
            self.vel_k_1 *= -1
        if speed_up:
            self.vel += self.SPEED_STEP
        if speed_down:
            self.vel -= self.SPEED_STEP
        if not_moving:
            self.vel_k_1 = 0

    def print_parameters(self, window):
        texts = ["CONFIG. PARAMS",
                 f"Speed: {self.vel:.2f} km/h",
                 f"\u0394T: {self.delta_t} s",
                 f"\u0394f increment: {self.ANGLE_STEP} °",
                 f"Lb: {self.lb} m",
                 f"Lf: {self.lf} m"]
        text_x, text_y = 20, 20
        i = 0
        for text in texts:
            text_rendered = FONT.render(text, True, WHITE)
            window.blit(text_rendered, (text_x, text_y + i))
            if i == 0:
                i += 20
            i += 15

    def apply_equations(self):
        self.delta_k_1 = self.delta_k
        self.x_k_1 = self.x_k
        self.y_k_1 = self.y_k
        self.phi_k_1 = self.phi

        self.beta_k_1 = atan2((self.lb * tan(deg2rad(self.delta_k_1))), (self.lf + self.lb))
        self.x_k = self.x_k_1 + self.vel_k_1/3.6 * self.delta_t * cos(self.phi_k_1 + self.beta_k_1)
        self.y_k = self.y_k_1 + self.vel_k_1/3.6 * self.delta_t * sin(self.phi_k_1 + self.beta_k_1)
        self.phi = (self.phi_k_1 + self.vel_k_1/3.6 * self.delta_t * cos(self.beta_k_1) * tan(
            deg2rad(self.delta_k_1)) / (self.lf + self.lb)) % (2 * pi)

        print(f"Beta: {rad2deg(self.beta_k_1):.3f}°, x: {self.x_k:.3f} m, y: {self.y_k:.3f} m, "
              f"heading_angle: {rad2deg(self.phi):.3f}°")

    def print_position(self, window):
        self.apply_equations()
        position_str = f"({self.x_k:.3f} m, {self.y_k:.3f} m, {(rad2deg(self.phi)):.3f} °)"
        position_rendered = FONT.render(position_str, True, GREEN)
        window.blit(position_rendered, (self.x_pos + 15, self.y_pos + 15))


def draw(window, car):
    WINDOW.fill(BLACK)
    car.draw(window)
    car.print_parameters(window)
    car.print_position(window)
    pygame.display.update()


def handle_movement(car, keys):
    # Check which keys are being pressed
    moving = False
    if keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
        moving = True
    if keys[pygame.K_UP] and not (keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
        car.move(up=True)
    if keys[pygame.K_LEFT] and keys[pygame.K_UP] and not keys[pygame.K_RIGHT]:
        car.move(up_left=True)
    if keys[pygame.K_RIGHT] and keys[pygame.K_UP] and not keys[pygame.K_LEFT]:
        car.move(up_right=True)
    if keys[pygame.K_DOWN] and not (keys[pygame.K_UP] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
        car.move(down=True)
    if keys[pygame.K_LEFT] and keys[pygame.K_DOWN] and not keys[pygame.K_RIGHT]:
        car.move(down_left=True)
    if keys[pygame.K_RIGHT] and keys[pygame.K_DOWN] and not keys[pygame.K_LEFT]:
        car.move(down_right=True)
    if keys[pygame.K_f] and car.vel < UPPER_SPEED_LIMIT and moving:
        car.move(speed_up=True)
    if keys[pygame.K_s] and car.vel > LOWER_SPEED_LIMIT and moving:
        car.move(speed_down=True)
    if not moving:
        car.move(not_moving=True)


def main(vehicle_speed, lf, lb, x0, y0, phi0, df0, dt):
    run = True
    clock = pygame.time.Clock()

    car = Car(vehicle_speed, lf, lb, x0, y0, phi0, df0, dt)
    while run:
        clock.tick(FPS)
        draw(WINDOW, car)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        handle_movement(car, keys)
    pygame.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Give parameters for the car")
    parser.add_argument('--vehicle_speed', type=int, help="Speed of the vehicle [km/h]")
    parser.add_argument('--lf', type=float, help="Distance from vehicle's center of mass to the front wheel axle [m]")
    parser.add_argument('--lb', type=float, help="Distance from vehicle's center of mass to the back wheel axle [m]")
    parser.add_argument('--x0', type=float, help="x-coordinate for the initial position [m]")
    parser.add_argument('--y0', type=float, help="y-coordinate for the initial position [m]")
    parser.add_argument('--phi0', type=float, help="Initial Heading Angle [°]")
    parser.add_argument('--df0', type=float, help="Initial front wheel rotation angle [°]")
    parser.add_argument('--dt', type=float, help="Sampling time interval [sec]")
    args = parser.parse_args()
    main(args.vehicle_speed, args.lf, args.lb, args.x0, args.y0, args.phi0, args.df0, args.dt)
