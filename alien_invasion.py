import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Класс для управления ресурсами и поведением игры."""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы."""
        pygame.init()
        self.settings = Settings()

        # небольшой режим окна
        # self.screen = pygame.display.set_mode(
        #     (self.settings.screen_width, self.settings.screen_height))

        # полноэкранный режим
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()


    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()

    def _check_events(self):
        """Обрабатывает нажатия клавиш и события мыши."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиш."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Реагирует на отпускание клавиш."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """Создание флота вторжения."""
        # Создание пришельца.
        alien = Alien(self)
        self.aliens.add(alien)

    def _update_bullets(self):
        """Обновляет позиции снарядов и уничтожает старые снаряды."""
        # Обновление позиций снарядов.
        self.bullets.update()

        # Удаление снарядов, вышедших за край экрана.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)


    def _update_screen(self):
        """Обновляет изображения на экране и отображает новый экран."""
        self.screen.fill(self.settings.bg_color)

        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Отображение последнего прорисованного экрана.
        pygame.display.flip()


if __name__ == '__main__':
    # Создание экземпляра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()