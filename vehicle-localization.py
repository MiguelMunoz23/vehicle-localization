#!/usr/bin/python3.8

"""
vehicle-localization.py

This Python script implements the equations for an autonomous car and uses pygame to visualize an animation.

Author: Miguel Angel Muñoz Rizo

Institution: Universidad de Monterrey
Subject: Advanced Robotics
Lecturer: Dr. Andrés Hernández Gutiérrez

Date of creation: 28 August 2022
"""

# Import useful libraries
import pygame

# Initialize pygame and constants
pygame.init()
FPS = 60

# Create a window
WIDTH, HEIGHT = 1000, 1000
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ackerman Steering Simulator | Advanced Robotics")

# Define colors
BLACK = (0, 0, 0)


class Car:
    CAR_WIDTH = 40
    CAR_HEIGHT = 20

    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load('car.png'), (self.CAR_WIDTH, self.CAR_HEIGHT))
        self.x = 0
        self.y = 0
        self.vel = 5  # 100 km/h

    def draw(self, window):
        # Display car image in the center of the screen and add the x and y coordinate
        window.blit(self.image, (WIDTH // 2 - self.CAR_WIDTH // 2 + self.x,
                                 HEIGHT // 2 - self.CAR_HEIGHT // 2 + self.y))

    def move(self, up):
        if up:
            self.x += self.vel
        else:
            self.x -= self.vel


def draw(window, car):
    window.fill(BLACK)
    car.draw(window)
    pygame.display.update()


def handle_movement(car, keys):
    if keys[pygame.K_UP]:
        car.move(up=True)
    if keys[pygame.K_DOWN]:
        car.move(up=False)


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
    main()
