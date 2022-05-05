from cfg import SCREEN_HEIGHT, SCREEN_WIDTH
from background.hill import Hill
from components.fire import Fire
from components.star import StarField
from background.mountain import Mountain
import pygame
import opensimplex
import sys, random, math


def main():
    pygame.init()
    screen = pygame.display.set_mode((960, 600))

    # Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((12, 20, 69))

    #Draw mountain
    mountain_base_color = pygame.Color((0, 0, 0))
    mountain_base_color.hsla = (random.randint(0, 360), 50, 50, 100)
    mountain = Mountain(mountain_base_color)
    mountain.draw(background)

    # Draw hill
    hill_base_color = pygame.Color((0, 0, 0))
    hill_base_color.hsla = (random.randint(0, 360), 50, 50, 100)
    hill = Hill(hill_base_color)
    hill.draw(background)



    # Randomness
    sunmoon = random.randint(0, 1)
    shape_x = random.randint(100, 900)
    shape_y = random.randint(80, 160)

    # Seed simplex noise
    opensimplex.seed(1234)

    # Draw fire
    fire = Fire(screen)

    # Draw star field
    starfield = StarField(screen)

    # Clock
    clock = pygame.time.Clock()

    screen.blit(background, (0, 0))

    while True:
        clock.tick(30)
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                opensimplex.seed(random.randint(0,2000))
                main()
        # drawing sun
        if sunmoon == 1:
            for i in range(15):
                pygame.draw.circle(screen, (255, 15 * i, 0), (shape_x, shape_y), 75 - (5 * i))
        # drawing moon
        else:
            pygame.draw.circle(screen, (229, 228, 226), (shape_x, shape_y), 75)
            pygame.draw.circle(screen, (192, 192, 192), (shape_x, shape_y), 65)

        fire.draw()
        starfield.draw()
        pygame.display.update()
main()
