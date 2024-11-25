import pygame
from settings import *
from collections import deque


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
        self.path_index = 0  # Индекс для отслеживания позиции в пути
    """ОБРАБОТКА МАРШРУТА ТРЕБУЕТ ДОРАБОТКИ"""
    def move_along_path(self, player_path):
        """Движение дивана по маршруту игрока с задержкой."""
        if self.paused > 0:
            self.paused -= 1
            return

        if len(player_path) > 30:  # Убедимся, что есть достаточная задержка
            target_state = player_path[0]  # Берем самую старую позицию
            target_x, target_y = target_state["x"], target_state["y"]

            # Двигаемся к следующей точке
            if self.rect.x < target_x:
                self.rect.x += min(self.speed, target_x - self.rect.x)
            elif self.rect.x > target_x:
                self.rect.x -= min(self.speed, self.rect.x - target_x)

            if self.rect.y < target_y:
                self.rect.y += min(self.speed, target_y - self.rect.y)
            elif self.rect.y > target_y:
                self.rect.y -= min(self.speed, self.rect.y - target_y)

            # Удаляем точку из пути, если она достигнута
            if abs(self.rect.x - target_x) < self.speed and abs(self.rect.y - target_y) < self.speed:
                player_path.popleft()

    def stop(self, duration):
        self.paused = duration

    def draw(self, screen):
        """Отрисовка дивана с использованием его изображения."""
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