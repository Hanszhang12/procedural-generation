from perlin_noise import PerlinNoise
import pygame, sys, random


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

class FireParticle:
    def __init__(self, x=100, y=500, r=5):
        self.r = r
        self.orig_radius = r
        self.x = x
        self.y = y
        self.layers = 2
        self.glow = 2
        self.surface = pygame.Surface((2 * self.r * self.layers ** 2 * self.glow, 2 * self.r * self.layers ** 2 * self.glow), pygame.SRCALPHA)
        self.burn_rate = random.randint(1, 4) * 0.1

    def update(self):
        self.orig_radius -= self.burn_rate
        self.y -= 6
        self.y += self.r
        self.x += random.randint(-self.r, self.r)
        self.r = int(self.orig_radius)
        if self.r <= 0:
            self.r = 1

    def draw(self):
        self.surface = pygame.Surface((2 * self.r * self.layers **2 * self.glow, 2 * self.r * self.layers **2 * self.glow), pygame.SRCALPHA)
        for particle in range(self.layers, -1, -1):
            radius = self.r * particle**2 * self.glow
            alpha = 255 - particle * (255 // self.layers - 5)
            if alpha <= 0:
                alpha = 0
            if self.r <= 4 and self.r > 2:
                color = (255, 0, 0, alpha)
            elif self.r == 2:
                color = (255, 160, 0, alpha)
            else:
                color = (75, 75, 75, alpha)
            pygame.draw.circle(self.surface, color, (self.surface.get_width() // 2, self.surface.get_height() // 2), radius)
        screen.blit(self.surface, self.surface.get_rect(center=(self.x, self.y)))

class Fire:
    def __init__(self, x=100, y=500, intensity = 2, particles= []):
        self.x = x
        self.y = y
        self.intensity = intensity
        self.particles = particles
        for i in range(self.intensity * 30):
            new_particle = FireParticle(self.x + random.randint(-3, 3), self.y, random.randint(1, 5))
            self.particles.append(new_particle)

    def draw(self):
        for particle in self.particles:
            if particle.orig_radius <= 0:
                self.particles.remove(particle)
                del particle
                new_particle = FireParticle(self.x + random.randint(-3, 3), self.y, random.randint(1, 5))
                self.particles.append(new_particle)
                continue
            particle.update()
            particle.draw()
fire = Fire()
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((960, 600))
    # #drawing sun
    # sun_x = random.randint(5, 50)
    # sun_y = random.randint(5, 10)
    # for i in range(15):
    #     pygame.draw.circle(screen, (255, 15 * i, 0), (100, 200), 75 - (5 * i))
    # #drawing moon
    # moon_x, moon_y, moon_r, blob_radius = 450, 200, 65, 5
    # pygame.draw.circle(screen, (229, 228, 226), (450, 200), 75)
    # pygame.draw.circle(screen, (192, 192, 192), (450, 200), 65)
    # #trying to build moon craters within bounds of moon's inner circle
    # blob_x = random.randint(moon_x-moon_r + blob_radius, moon_x+moon_r-blob_radius)
    # blob_y = random.randint(moon_y-moon_r+blob_radius, moon_y+moon_r-blob_radius)
    # pygame.draw.circle(screen, (112, 128, 144), (blob_x, blob_y), blob_radius)


    clock = pygame.time.Clock()
    particle1 = LayerBGStar()

    #blinking star system
    #array of coordinates of the center of each star
    curr_stars = []
    for j in range(20):
        s_x, s_y, s_c = random.randint(0, 960), random.randint(0, 200), 255
        curr_stars.append((s_x, s_y, s_c))
        pygame.draw.circle(screen, (s_c, s_c, s_c), (s_x, s_y), 5)

    PARTICLE_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(PARTICLE_EVENT, 10)

    sunmoon = random.randint(0, 1)

    while True:
        screen.fill((12, 20, 69))
        pygame.draw.ellipse(screen, (85, 127, 70), pygame.Rect(-100, 350, 450, 350))
        pygame.draw.ellipse(screen, (85, 127, 70), pygame.Rect(-50, 350, 850, 450))
        pygame.draw.ellipse(screen, (85, 127, 70), pygame.Rect(500, 350, 700, 600))
        pygame.draw.rect(screen, (97, 112, 77), pygame.Rect(0, 450, 960, 150))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == PARTICLE_EVENT:
                particle1.add_particles()

        for s_i in range(len(curr_stars)):
            s_x, s_y, s_c = curr_stars[s_i]
            pygame.draw.circle(screen, (s_c - 15, s_c - 15, s_c - 15), (s_x, s_y), 5)
            if s_c <= 80:
                pygame.draw.circle(screen, (12, 20, 69), (s_x, s_y), 5)
                curr_stars[s_i] = (random.randint(0, 960), random.randint(0, 200), 255)
            else:
                curr_stars[s_i] = (s_x, s_y, s_c - 15)

        #drawing sun
        if sunmoon:
            sun_x = random.randint(5, 50)
            sun_y = random.randint(5, 10)
            for i in range(15):
                pygame.draw.circle(screen, (255, 15 * i, 0), (100, 100), 75 - (5 * i))
        #drawing moon
        else:
            moon_x, moon_y, moon_r, blob_radius = 450, 200, 65, 5
            pygame.draw.circle(screen, (229, 228, 226), (100, 100), 75)
            pygame.draw.circle(screen, (192, 192, 192), (100, 100), 65)
        fire.draw()

        particle1.emit()
        pygame.display.update()
        clock.tick(30)
