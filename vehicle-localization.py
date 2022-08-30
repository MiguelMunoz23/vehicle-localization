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

from math import sin, cos

# Import useful libraries
import pygame
import argparse
from numpy import deg2rad
import time

# Initialize pygame and constants
pygame.init()
FPS = 60

# Create a window
WIDTH, HEIGHT = 1000, 1000
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ackerman Steering Simulator | Advanced Robotics")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)


class Car:
    VEL = 1  # 100 km/h
    ANGLE_STEP = 1.2

    def __init__(self):
        self.width = 40
        self.height = 20
        self.x = 0
        self.y = 0
        self.past_positions = []
        self.car_x_center = WIDTH // 2 - self.width // 2
        self.car_y_center = HEIGHT // 2 - self.height // 2
        self.angle = 0
        self.x_vel = 0
        self.y_vel = 0
        self.image = None
        self.bounding_box = None

    def draw(self, window):
        # Rotate the image with respect to the angle
        self.image = pygame.transform.rotate(
            pygame.transform.scale(pygame.image.load('car.png'), (self.width, self.height)), self.angle)
        # Bounding box
        self.bounding_box = self.image.get_bounding_rect()
        self.bounding_box.center = self.car_x_center + self.x + self.image.get_width()//2,\
                                   self.car_y_center + self.y + self.image.get_height()//2
        pygame.draw.rect(window, GREEN, self.bounding_box, 1)
        # Code for leaving trail
        self.past_positions.append([self.bounding_box.center[0], self.bounding_box.center[1]])
        for point in self.past_positions:
            pygame.draw.circle(window, YELLOW, point, 2)
        # Display car image in the center of the screen and add the x and y coordinate
        window.blit(self.image, (self.car_x_center + self.x, self.car_y_center + self.y))

    def move(self, up=None, up_left=None, up_right=None, down=None, down_left=None, down_right=None):
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


def draw(window, car):
    WINDOW.fill(BLACK)
    car.draw(window)
    pygame.display.update()


def handle_movement(car, keys):
    # Check which keys are being pressed
    if keys[pygame.K_UP] and not(keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
        car.move(up=True)
    if keys[pygame.K_LEFT] and keys[pygame.K_UP]:
        car.move(up_left=True)
    if keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
        car.move(up_right=True)
    if keys[pygame.K_DOWN] and not(keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
        car.move(down=True)
    if keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
        car.move(down_left=True)
    if keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
        car.move(down_right=True)


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
