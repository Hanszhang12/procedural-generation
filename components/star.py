from cfg import SCREEN_HEIGHT, SCREEN_WIDTH
import pygame
import random


class StarParticle:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.initial_x = x
        self.initial_y = y
        self.x = x
        self.y = y
        self.v_x = -15
        self.v_y = 5
        self.a_x = 0.5
        self.a_y = 0.15
        self.elapsed = 0
        self.duration = 12
        self.timestep = 0.25
        self.fade_out = 5
        self.trails = []

    def update(self):
        # store previous position for trails
        self.trails.append((self.x, self.y))

        # increase timestep
        self.elapsed += self.timestep

        if self.elapsed <= self.duration + 4:
            # apply movement
            self.x += self.v_x * self.timestep
            self.y += self.v_y * self.timestep

            # apply de/acceleration
            self.v_x += self.a_x * self.timestep

            # cannot turn positive
            self.v_x = min(self.v_x, 0)

            self.v_y += self.a_y * self.timestep

    def draw(self):
        self.surface = pygame.Surface(
            self.screen.get_size(),
            pygame.SRCALPHA,
        )

        if self.elapsed <= self.duration:
            i = 0
            for trail in self.trails:
                pygame.draw.circle(
                    self.surface,
                    (255, 255, 255, (i / len(self.trails) * 50)),
                    (trail[0], trail[1]),
                    2,
                )
                i += 1

            pygame.draw.circle(
                self.surface,
                (255, 255, 255, (self.elapsed / self.duration * 255)),
                (self.x, self.y),
                4,
            )

        else:
            i = 0
            for trail in self.trails:
                pygame.draw.circle(
                    self.surface,
                    (
                        255,
                        255,
                        255,
                        max(
                            (i / len(self.trails) * 50)
                            - (self.elapsed - self.duration)
                            / self.fade_out
                            * (i / len(self.trails) * 50),
                            0,
                        ),
                    ),
                    (trail[0], trail[1]),
                    2,
                )
                i += 1

            pygame.draw.circle(
                self.surface,
                (
                    255,
                    255,
                    255,
                    max(
                        (self.elapsed / self.duration * 255)
                        - (self.elapsed - self.duration)
                        / self.fade_out
                        * (self.elapsed / self.duration * 255),
                        0,
                    ),
                ),
                (self.x, self.y),
                4,
            )

        self.screen.blit(self.surface, (0, 0))


class StarField:
    def __init__(self, screen):
        self.screen = screen
        self.stars = []
        self.max_star = 10

    def create_new_star(self):
        new_star = StarParticle(
            self.screen, random.randint(100, SCREEN_WIDTH), random.randint(0, 150)
        )
        self.stars.append(new_star)

    def draw(self):
        new_star = random.randint(0, 50) < 8 and len(self.stars) < self.max_star

        if new_star:
            self.create_new_star()

        for star in self.stars:
            if star.elapsed >= star.duration + star.fade_out:
                self.stars.remove(star)
                self.create_new_star()
                continue

            star.update()
            star.draw()
