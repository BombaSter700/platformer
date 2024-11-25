import pygame
from settings import *
from collections import deque

pygame.init()

# Состояния игры
MENU = "menu"
PLAYING = "playing"
GAME_OVER = "game_over"

class Game:
    def __init__(self):
        self.images = load_images("C:\\Users\\Sanek\\Desktop\\платформер\\images")
        self.images["main_background"] = pygame.transform.scale(
            self.images["main_background"], (WIDTH, HEIGHT)
        )
        self.images["couch"] = pygame.transform.scale(
            self.images["couch"], (DIVAN_WIDTH, DIVAN_HEIGHT)
        )
        self.images["coffee"] = self.images["coffee"]
        self.images["clock"] = self.images["clock"]

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Диванная революция")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = MENU  # Начальное состояние
        self.score = 0
        self.player_path = deque(maxlen=100) #Очередь записи маршрута игрока 

    def run(self):
        while self.running:
            if self.state == MENU:
                self.show_menu()
            elif self.state == PLAYING:
                self.play_game()
            elif self.state == GAME_OVER:
                self.show_game_over()
            self.clock.tick(FPS)
        pygame.quit()

    def show_menu(self):
        # Главный экран
        self.screen.fill(WHITE)
        font = pygame.font.Font(None, 72)
        title_text = font.render("Диванная революция", True, (0, 0, 0))
        start_text = font.render("Нажмите любую клавишу, чтобы начать", True, (0, 0, 0))
        self.screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
        self.screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                if event.type == pygame.KEYDOWN:  # Событие для любой клавиши
                    self.state = PLAYING
                    waiting = False

    def play_game(self):
        # Создание игрового уровня
        player = Player(100, HEIGHT - PLAYER_HEIGHT - 20)
        self.couch = Couch(50, HEIGHT - DIVAN_HEIGHT, self.images["couch"])  # Начальное положение дивана
        platforms = [Platform(0, HEIGHT - 20, WIDTH),
                    Platform(300, HEIGHT - 100, PLATFORM_WIDTH),
                    Platform(500, HEIGHT - 200, PLATFORM_WIDTH)]
        bonuses = [Coffee(350, HEIGHT - 120, self.images["coffee"], "coffee"),
                Clock(550, HEIGHT - 220, self.images["clock"], "alarm")]
        
        self.couch.move_along_path(list(self.player_path))

        safe_timer = 30  # Таймер для безопасного старта

        """ОСНОВНОЙ ЦИКЛ ИГРЫ"""
        while self.state == PLAYING:
            self.screen.blit(self.images["main_background"], (0, 0))
            self.couch.draw(self.screen)

            self.player_path.append({
            "x": player.rect.x,
            "y": player.rect.y,
            "on_ground": player.on_ground,
            "velocity_y": player.velocity_y
            }) #в каждом кадре запись коорд и действий игрока

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.state = None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.jump()


            # Обновление игрока, дивана и уровня
            keys = pygame.key.get_pressed()
            player.move(keys)
            player.apply_gravity()
            player.update()

            self.couch.move_towards(player.rect.x)

            # Проверка столкновений
            player.on_ground = False
            for platform in platforms:
                if player.rect.colliderect(platform.rect) and player.velocity_y > 0:
                    player.velocity_y = 0
                    player.rect.bottom = platform.rect.top
                    player.on_ground = True

            for bonus in bonuses[:]:
                if player.rect.colliderect(bonus.rect):
                    if bonus.type == "coffee":
                        player.speed += 3
                    elif bonus.type == "alarm":
                        self.couch.stop(180)
                    bonuses.remove(bonus)

            # Проверка проигрыша (после таймера безопасного старта)
            if safe_timer <= 0 and self.couch.rect.colliderect(player.rect):
                self.state = GAME_OVER
                break
            safe_timer -= 1

            # Прокрутка уровня
            if player.rect.centerx > WIDTH // 2 and player.velocity_x > 0:
                for platform in platforms:
                    platform.rect.x -= player.velocity_x
                for bonus in bonuses:
                    bonus.rect.x -= player.velocity_x
                self.couch.rect.x -= player.velocity_x
                player.rect.x = WIDTH // 2 - PLAYER_WIDTH // 2

            # Отрисовка объектов
            for platform in platforms:
                platform.draw(self.screen)
            for bonus in bonuses:
                bonus.draw(self.screen)

            pygame.draw.rect(self.screen, BLUE, player.rect)

            # Отображение очков
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {self.score}", True, (0, 0, 0))
            self.screen.blit(score_text, (10, 10))

            pygame.display.flip()
            self.clock.tick(FPS)



    def show_game_over(self):
        # Экран проигрыша
        self.screen.fill(WHITE)
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("Вы проиграли!", True, (255, 0, 0))
        restart_text = font.render("Нажмите R, чтобы начать заново", True, (0, 0, 0))
        self.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
        self.screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # R для рестарта
                    self.state = MENU


if __name__ == "__main__":
    from game_objects import Player, Couch, Platform, Coffee, Clock
    from assets import load_images
    game = Game()
    game.run()
