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
    def __init__(self, x, y, image):
        self.rect = pygame.Rect(x, y, DIVAN_WIDTH, DIVAN_HEIGHT)
        self.speed = 2
        self.paused = 0
        self.image = image
        self.path_index = 0  # Индекс для текущего состояния

    def move_along_path(self, player_path):
         if self.path_index < len(player_path):
            state = player_path[self.path_index]
            self.rect.x = state["x"]
            self.rect.y += state["velocity_y"]  # Применяем гравитацию
            if state["on_ground"]:
                self.rect.y = state["y"]  # Ставим диван на платформу
            self.path_index += 1
            
    def move_towards(self, target_x):
        if self.paused > 0:
            self.paused -= 1
        else:
            if self.rect.x < target_x - 100:
                self.rect.x += self.speed

    def stop(self, duration):
        self.paused = duration

    def draw(self, screen):
        # Отрисовка дивана с использованием его картинки
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Platform:
    def __init__(self, x, y, width):
        self.rect = pygame.Rect(x, y, width, PLATFORM_HEIGHT)

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self.rect)


class Coffee:
    def __init__(self, x, y, image, bonus_type):
        self.rect = pygame.Rect(x, y, 20, 35)
        self.image = image
        self.type = bonus_type

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Clock:
    def __init__(self, x, y, image, bonus_type):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.image = image
        self.type = bonus_type

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))