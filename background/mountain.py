import pygame
import opensimplex
from cfg import SCREEN_HEIGHT, SCREEN_WIDTH


class Mountain:
    def __init__(self, base_color):
        self.base_color = base_color

    def draw(self, background):
        points1, points2, points3, points4 = self.generate_points()

        mountain_color_1 = pygame.Color((0, 0, 0))
        mountain_color_2 = pygame.Color((0, 0, 0))
        mountain_color_3 = pygame.Color((0, 0, 0))
        mountain_color_4 = pygame.Color((0, 0, 0))

        mountain_color_1.hsla = self.base_color.hsla
        mountain_color_2.hsla = tuple(
            map(lambda i, j: i - j, self.base_color.hsla, (0, 20, 10, 0))
        )
        mountain_color_3.hsla = tuple(
            map(lambda i, j: i - j, self.base_color.hsla, (0, 25, 20, 0))
        )
        mountain_color_4.hsla = tuple(
            map(lambda i, j: i - j, self.base_color.hsla, (0, 30, 30, 0))
        )

        pygame.draw.polygon(background, mountain_color_1, points1)
        pygame.draw.polygon(background, mountain_color_2, points2)
        pygame.draw.polygon(background, mountain_color_3, points3)
        pygame.draw.polygon(background, mountain_color_4, points4)


    def generate_points(self):
        points1 = [[0, SCREEN_HEIGHT]]
        points2 = [[0, SCREEN_HEIGHT]]
        points3 = [[0, SCREEN_HEIGHT]]
        points4 = [[0, SCREEN_HEIGHT]]

        for i in range(SCREEN_WIDTH):
            points1.append([i, 300 + 100 * opensimplex.noise2(0.008 * i, 0)])
            points2.append([i, 320 + 100 * opensimplex.noise2(0.008 * i, 0.02)])
            points3.append([i, 360 + 100 * opensimplex.noise2(0.008 * i, 0.04)])
            points4.append([i, 420 + 100 * opensimplex.noise2(0.008 * i, 0.04)])

        points1.append([SCREEN_WIDTH, SCREEN_HEIGHT])
        points2.append([SCREEN_WIDTH, SCREEN_HEIGHT])
        points3.append([SCREEN_WIDTH, SCREEN_HEIGHT])
        points4.append([SCREEN_WIDTH, SCREEN_HEIGHT])

        return points1, points2, points3, points4
