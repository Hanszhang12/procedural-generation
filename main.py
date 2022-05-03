import pygame, sys, random
import opensimplex

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 960


class LayerHill:
    def __init__(self):
        pass

    def draw(self, screen):
        points1, points2, points3 = self.generate_points()
        print(points1)
        pygame.draw.lines(screen, (255, 255, 255), False, points1, width=1)
        pygame.draw.lines(screen, (0, 0, 0), False, points2, width=1)
        pygame.draw.lines(screen, (255, 255, 255), False, points3, width=1)

    def generate_points(self):
        points1 = []
        points2 = []
        points3 = []

        for i in range(SCREEN_WIDTH):
            points1.append([i, 520 + 250 * opensimplex.noise2(0.005 * i, 0)])
            points2.append([i, 500 + 250 * opensimplex.noise2(0.005 * i, 0.02)])
            points3.append([i, 480 + 250 * opensimplex.noise2(0.005 * i, 0.04)])

        return points1, points2, points3


class LayerBGStar:
    def __init__(self):
        self.particles = []
        self.surface = pygame.transform.scale(
            pygame.image.load("star.png").convert_alpha(), (10, 10)
        )
        self.width = self.surface.get_rect().width
        self.height = self.surface.get_rect().height
        self.count = 0

    def emit(self):
        if self.particles:
            self.delete_particles()
            for particle in self.particles:
                particle[0].x += particle[1]
                particle[0].y += particle[2]
                particle[3] -= 0.2
                screen.blit(self.surface, particle[0])

    def add_particles(self):
        if self.count < 20:
            self.count += 1
            pos_x = random.randint(0, 960)
            pos_y = random.randint(0, 200)
            direction_x = 0
            direction_y = 0
            lifetime = 1
            particle_rect = pygame.Rect(int(pos_x), int(pos_y), self.width, self.height)
            self.particles.append([particle_rect, direction_x, direction_y, lifetime])

    def delete_particles(self):
        particle_copy = [particle for particle in self.particles if particle[3] > 0]
        self.particles = particle_copy


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((960, 600))
    screen.fill((12, 20, 69))
    #drawing sun
    sun_x = random.randint(5, 50)
    sun_y = random.randint(5, 10)
    for i in range(15):
        pygame.draw.circle(screen, (255, 15 * i, 0), (100, 200), 75 - (5 * i))
    #drawing moon
    moon_x, moon_y, moon_r, blob_radius = 450, 200, 65, 5
    pygame.draw.circle(screen, (229, 228, 226), (450, 200), 75)
    pygame.draw.circle(screen, (192, 192, 192), (450, 200), 65)
    #trying to build moon craters within bounds of moon's inner circle
    blob_x = random.randint(moon_x-moon_r + blob_radius, moon_x+moon_r-blob_radius)
    blob_y = random.randint(moon_y-moon_r+blob_radius, moon_y+moon_r-blob_radius)
    pygame.draw.circle(screen, (112, 128, 144), (blob_x, blob_y), blob_radius)

    pygame.draw.ellipse(screen, (85, 127, 70), pygame.Rect(-100, 350, 450, 350))
    pygame.draw.ellipse(screen, (85, 127, 70), pygame.Rect(-50, 350, 850, 450))
    pygame.draw.ellipse(screen, (85, 127, 70), pygame.Rect(500, 350, 700, 600))
    pygame.draw.rect(screen, (97, 112, 77), pygame.Rect(0, 450, 960, 150))

    # Seed simplex noise
    opensimplex.seed(1234)

    # Draw hill
    hill = LayerHill()
    hill.draw(screen)

    clock = pygame.time.Clock()
    particle1 = LayerBGStar()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(120)
