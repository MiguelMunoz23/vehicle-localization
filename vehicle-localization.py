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
    VEL = 1  # 100 km/h
    ANGLE_STEP = 1.2

    def __init__(self):
        self.x = 0
        self.y = 0
        self.angle = 0
        self.image = None

    def draw(self, window):
        self.image = pygame.transform.rotate(
            pygame.transform.scale(pygame.image.load('car.png'), (self.CAR_WIDTH, self.CAR_HEIGHT)), self.angle)
        # Display car image in the center of the screen and add the x and y coordinate
        window.blit(self.image, (WIDTH // 2 - self.CAR_WIDTH // 2 + self.x,
                                 HEIGHT // 2 - self.CAR_HEIGHT // 2 + self.y))

    def move(self, up=None, up_left=None, up_right=None, down=None, down_left=None, down_right=None):
        # Check every condition and move the car
        if up:
            self.x += self.VEL
        if up_left:
            self.x += self.VEL
            self.angle += self.ANGLE_STEP
        if up_right:
            self.x += self.VEL
            self.angle -= self.ANGLE_STEP
        if down:
            self.x -= self.VEL
        if down_left:
            self.x -= self.VEL
            self.angle += self.ANGLE_STEP
        if down_right:
            self.x -= self.VEL
            self.angle -= self.ANGLE_STEP


def draw(window, car):
    window.fill(BLACK)
    car.draw(window)
    pygame.display.update()


def handle_movement(car, keys):
    # Check which keys are being pressed
    if keys[pygame.K_UP]:
        car.move(up=True)
    if keys[pygame.K_LEFT] and keys[pygame.K_UP]:
        car.move(up_left=True)
    if keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
        car.move(up_right=True)
    if keys[pygame.K_DOWN]:
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
    main()
