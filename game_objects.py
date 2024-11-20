import pygame
from settings import *

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = 5
        self.on_ground = False

    def move(self, keys):
        self.velocity_x = 0
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.velocity_x = -self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < WIDTH - PLAYER_WIDTH:
            self.velocity_x = self.speed

    def jump(self):
        if self.on_ground:
            self.velocity_y = -15
            self.on_ground = False

    def apply_gravity(self):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

    def update(self):
        self.rect.x += self.velocity_x


class Couch:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, DIVAN_WIDTH, DIVAN_HEIGHT)
        self.speed = 2
        self.paused = 0

    def move_towards(self, target_x):
        if self.paused > 0:
            self.paused -= 1
        else:
            if self.rect.x < target_x - 100:
                self.rect.x += self.speed

    def stop(self, duration):
        self.paused = duration


class Platform:
    def __init__(self, x, y, width):
        self.rect = pygame.Rect(x, y, width, PLATFORM_HEIGHT)

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self.rect)


class Bonus:
    def __init__(self, x, y, bonus_type):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.type = bonus_type

    def draw(self, screen):
        color = ORANGE if self.type == "coffee" else BLUE
        pygame.draw.rect(screen, color, self.rect)
