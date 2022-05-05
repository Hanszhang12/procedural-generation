import pygame
import random


class FireParticle:
    def __init__(self, screen, x=100, y=500, r=5):
        self.screen = screen
        self.x = x
        self.y = y

        self.prev_x = x
        self.prev_y = y

        self.r = r
        self.current_radius = r

        self.layers = 2
        self.glow = 2
        self.surface = pygame.Surface(
            (
                2 * self.r * self.layers**2 * self.glow,
                2 * self.r * self.layers**2 * self.glow,
            ),
            pygame.SRCALPHA,
        )

        # How fast the the fire particle decay
        self.burn_rate = random.randint(1, 4) * 0.1

    def update(self):
        self.x += random.randint(-self.r, self.r)
        self.y -= random.randint(4, 7)

        self.current_radius -= self.burn_rate
        self.r = int(self.current_radius)

        if self.r <= 0:
            self.r = 1

    def draw(self):
        self.surface = pygame.Surface(
            (
                2 * self.r * self.layers**2 * self.glow,
                2 * self.r * self.layers**2 * self.glow,
            ),
            pygame.SRCALPHA,
        )

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

            pygame.draw.circle(
                self.surface,
                color,
                (self.surface.get_width() // 2, self.surface.get_height() // 2),
                radius,
            )

        self.screen.blit(self.surface, self.surface.get_rect(center=(self.x, self.y)))


class Fire:
    def __init__(self, screen, x=100, y=500, intensity=2, particles=[]):
        self.screen = screen
        self.surface = pygame.Surface(
            self.screen.get_size(),
            pygame.SRCALPHA,
        )
        self.x = x
        self.y = y

        # Controls how many fire particle exist
        self.intensity = intensity
        self.particles = particles

        for _ in range(self.intensity * 30):
            self.create_new_particle()

    def create_new_particle(self):
        new_particle = FireParticle(
            self.screen, self.x + random.randint(-3, 3), self.y, random.randint(1, 5)
        )
        self.particles.append(new_particle)

    def draw(self):
        pygame.draw.ellipse(
            self.screen,
            (255, 255, 255),
            pygame.Rect(self.x - 50, self.y, 100, 30),
        )

        pygame.draw.ellipse(
            self.screen,
            (0, 0, 0),
            pygame.Rect(self.x - 35, self.y + 5, 70, 20),
        )

        for particle in self.particles:
            if particle.current_radius <= 0:
                self.particles.remove(particle)
                self.create_new_particle()
                continue

            particle.update()
            particle.draw()
