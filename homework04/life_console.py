import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        height, width = screen.getmaxyx()
        # Рисуем горизонтальные границы
        for x in range(1, width - 1):
            screen.addch(0, x, curses.ACS_HLINE)
            screen.addch(height - 1, x, curses.ACS_HLINE)

        # Рисуем вертикальные границы
        for y in range(1, height - 1):
            screen.addch(y, 0, curses.ACS_VLINE)
            screen.addch(y, width - 2, curses.ACS_VLINE)

        # Рисуем углы
        screen.addch(0, 0, curses.ACS_ULCORNER)
        screen.addch(0, width - 2, curses.ACS_URCORNER)
        screen.addch(height - 1, 0, curses.ACS_LLCORNER)
        screen.addch(height - 1, width - 2, curses.ACS_LRCORNER)

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        height, width = screen.getmaxyx()

        # Вычисляем смещение для центрирования поля
        start_y = (height - self.life.rows) // 2
        start_x = (width - 1 - self.life.cols) // 2

        # Проверяем, помещается ли поле в окно
        if start_y <= 0 or start_x <= 0:
            screen.addstr(1, 1, "Window too small!")
            return

        # Отображаем клетки
        for y in range(self.life.rows):
            for x in range(self.life.cols):
                screen_y = start_y + y
                screen_x = start_x + x

                # Проверяем, что координаты в пределах окна
                if 0 < screen_y < height - 1 and 0 < screen_x < width - 2:

                    if self.life.curr_generation[y][x]:
                        screen.addch(screen_y, screen_x, "█")
                    else:
                        screen.addch(screen_y, screen_x, " ")

        # Отображаем информацию о поколении
        info = f"Generation: {self.life.generations} | Press 'q' to quit"
        if len(info) < width - 2:
            screen.addstr(height - 2, 1, info)

    def _handle_input(self, screen) -> bool:
        """
        Обработка ввода пользователя.
        Возвращает True, если игра должна продолжаться, False - если завершиться.
        """
        key = screen.getch()

        # Выход по нажатию 'q' или 'Q'
        if key == ord("q") or key == ord("Q"):
            return False

        return True

    def _check_game_over(self, screen) -> bool:
        """
        Проверка условий завершения игры.
        Возвращает True, если игра должна завершиться.
        """
        if self.life.is_max_generations_exceeded:
            height, width = screen.getmaxyx()
            if height > 3 and width > 30:
                screen.addstr(1, 1, "Max generations reached! You can exit")
            return True

        if not self.life.is_changing:
            height, width = screen.getmaxyx()
            if height > 3 and width > 30:
                screen.addstr(1, 1, "No more changes! You can exit")
            return True

        return False

    def run(self) -> None:
        screen = curses.initscr()
        try:
            # Настройки curses
            curses.noecho()  # Не отображать вводимые символы
            curses.cbreak()  # Режим cbreak (немедленный ввод)
            screen.keypad(True)  # Включить обработку специальных клавиш
            curses.curs_set(0)  # Скрыть курсор

            # Включаем неблокирующий ввод
            screen.nodelay(True)

            # Основной игровой цикл
            running = True
            while running:
                # Очищаем экран
                screen.clear()

                # Рисуем рамку и поле
                self.draw_borders(screen)
                self.draw_grid(screen)

                # Обновляем экран
                screen.refresh()

                # Обрабатываем ввод
                if not self._handle_input(screen):
                    break

                # Проверяем условия завершения игры
                if self._check_game_over(screen):
                    # Переключаем в блокирующий режим для ожидания нажатия
                    screen.nodelay(False)
                    screen.getch()  # Ждем любое нажатие
                    break

                # Выполняем шаг игры
                self.life.step()

                # Задержка для контроля скорости (100 мс)
                curses.napms(100)

        finally:
            # Восстанавливаем настройки терминала
            curses.nocbreak()
            screen.keypad(False)
            curses.echo()
            curses.endwin()


if __name__ == "__main__":
    # Запуск консольной версии
    life = GameOfLife(size=(15, 25), randomize=True, max_generations=100)
    console = Console(life)
    console.run()
