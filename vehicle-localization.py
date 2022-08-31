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
from math import sin, cos, atan, tan

# Import useful libraries
import pygame
from numpy import deg2rad

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
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)


class Car:
    VEL = 1  # 100 [km/h]
    ANGLE_STEP = 1.2  # [°]
    DELTA_T = 0.1  # [sec]
    LF = 1.4  # [m]
    LB = 1.2  # [m]

    def __init__(self):
        self.width = 40
        self.height = 20
        self.x = 0
        self.y = 0
        self.past_positions = []
        self.x_pos = 0
        self.y_pos = 0
        self.angle = 0
        self.x_vel = 0
        self.y_vel = 0
        self.image = None
        self.beta_k = 0
        self.x_k = 0
        self.y_k = 0
        self.phi = 0

    def draw(self, window):
        self.x_pos = WIDTH // 2 + self.x
        self.y_pos = HEIGHT // 2 + self.y

        # Rotate the image with respect to the angle
        self.image = pygame.transform.rotate(
            pygame.transform.scale(pygame.image.load('car.png'), (self.width, self.height)), self.angle)

        # Leaving trail
        self.past_positions.append([self.x_pos, self.y_pos])
        for point in self.past_positions:
            pygame.draw.circle(window, YELLOW, point, 2)

        # Display car image in the center of the screen and add the x and y coordinate
        window.blit(self.image, self.image.get_rect(center=(self.x_pos, self.y_pos)))

    def move(self, up=None, up_left=None, up_right=None, down=None, down_left=None, down_right=None, speed_up=None,
             speed_down=None):
        # Check every condition and move the car accordingly
        self.x_vel = self.VEL * cos(deg2rad(self.angle))
        self.y_vel = self.VEL * sin(deg2rad(self.angle))
        if up:  # Forward
            self.x += self.x_vel
            self.y -= self.y_vel
        if up_left:  # Forward left
            self.x += self.x_vel
            self.y -= self.y_vel
            self.angle += self.ANGLE_STEP
        if up_right:  # Forward right
            self.x += self.x_vel
            self.y -= self.y_vel
            self.angle -= self.ANGLE_STEP
        if down:  # Backwards
            self.x -= self.x_vel
            self.y += self.y_vel
        if down_left:  # Backwards left
            self.x -= self.x_vel
            self.y += self.y_vel
            self.angle -= self.ANGLE_STEP
        if down_right:  # Backwards right
            self.x -= self.x_vel
            self.y += self.y_vel
            self.angle += self.ANGLE_STEP
        if speed_up:
            self.VEL += 0.1
        if speed_down:
            self.VEL -= 0.1

    def print_parameters(self, window):
        texts = ["CONFIG. PARAMS",
                 f"Speed: {(self.VEL*100):.2f} km/h",
                 f"\u0394T: {self.DELTA_T} s",
                 f"\u0394f increment: {self.ANGLE_STEP} °",
                 f"Lb: {self.LB} m",
                 f"Lf: {self.LF} m"]
        text_x, text_y = 20, 20
        i = 0
        for text in texts:
            text_rendered = FONT.render(text, True, WHITE)
            window.blit(text_rendered, (text_x, text_y + i))
            if i == 0:
                i += 20
            i += 15

    def apply_equations(self):
        self.beta_k = atan(self.LB * tan(self.angle) / (self.LF + self.LB))
        self.x_k = self.x + self.VEL * self.DELTA_T * cos(self.angle + self.beta_k)
        self.y_k = self.y + self.VEL * self.DELTA_T * cos(self.angle + self.beta_k)
        self.phi = self.phi + self.VEL * self.DELTA_T * (cos(self.beta_k) * tan(self.angle) / (self.LF + self.LB))

    def print_position(self, window):
        self.apply_equations()
        position_str = f"({self.x_k:.3f} m, {self.y_k:.3f} m, {self.phi:.3f} °)"
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
    if keys[pygame.K_UP] and not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
        car.move(up=True)
    if keys[pygame.K_LEFT] and keys[pygame.K_UP]:
        car.move(up_left=True)
    if keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
        car.move(up_right=True)
    if keys[pygame.K_DOWN] and not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
        car.move(down=True)
    if keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
        car.move(down_left=True)
    if keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
        car.move(down_right=True)
    if keys[pygame.K_f] and car.VEL <= 3 and (keys[pygame.K_UP] or keys[pygame.K_DOWN] or
                                              keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
        car.move(speed_up=True)
    if keys[pygame.K_s] and car.VEL > 0.1 and (keys[pygame.K_UP] or keys[pygame.K_DOWN] or
                                               keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
        car.move(speed_down=True)


def main():
    run = True
    clock = pygame.time.Clock()

    car = Car()
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
    main()
