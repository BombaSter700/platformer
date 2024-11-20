import pygame
from settings import *

pygame.init()

# Состояния игры
MENU = "menu"
PLAYING = "playing"
GAME_OVER = "game_over"

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Диванная революция")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = MENU  # Начальное состояние
        self.score = 0

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
        couch = Couch(50, HEIGHT - DIVAN_HEIGHT)  # Начальное положение дивана
        platforms = [Platform(0, HEIGHT - 20, WIDTH),
                    Platform(300, HEIGHT - 100, PLATFORM_WIDTH),
                    Platform(500, HEIGHT - 200, PLATFORM_WIDTH)]
        bonuses = [Bonus(350, HEIGHT - 120, "coffee"),
                Bonus(550, HEIGHT - 220, "alarm")]

        safe_timer = 30  # Таймер для безопасного старта

        while self.state == PLAYING:
            self.screen.fill(WHITE)

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

            couch.move_towards(player.rect.x)

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
                        couch.stop(180)
                    bonuses.remove(bonus)

            # Проверка проигрыша (после таймера безопасного старта)
            if safe_timer <= 0 and couch.rect.colliderect(player.rect):
                self.state = GAME_OVER
                break
            safe_timer -= 1

            # Прокрутка уровня
            if player.rect.centerx > WIDTH // 2 and player.velocity_x > 0:
                for platform in platforms:
                    platform.rect.x -= player.velocity_x
                for bonus in bonuses:
                    bonus.rect.x -= player.velocity_x
                couch.rect.x -= player.velocity_x
                player.rect.x = WIDTH // 2 - PLAYER_WIDTH // 2

            # Отрисовка объектов
            for platform in platforms:
                platform.draw(self.screen)
            for bonus in bonuses:
                bonus.draw(self.screen)

            pygame.draw.rect(self.screen, BLUE, player.rect)
            pygame.draw.rect(self.screen, RED, couch.rect)

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
    from game_objects import Player, Couch, Platform, Bonus
    game = Game()
    game.run()
