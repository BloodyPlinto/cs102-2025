import pygame  # type: ignore

from life import GameOfLife
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.width = life.cols * cell_size
        self.height = life.rows * cell_size
        self.paused = False
        self.running = True
        self.clock = pygame.time.Clock()

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Conway's Game of Life")

    def draw_lines(self) -> None:
        # Copy from previous assignment
        black = pygame.Color("black")
        rows_px, cols_px = self.life.rows * self.cell_size, self.life.cols * self.cell_size

        # Вертикальные линии
        for x in range(0, cols_px + 1, self.cell_size):
            pygame.draw.line(self.screen, black, (x, 0), (x, rows_px), 1)

        # Горизонтальные линии
        for y in range(0, rows_px + 1, self.cell_size):
            pygame.draw.line(self.screen, black, (0, y), (cols_px, y), 1)

    def draw_grid(self) -> None:
        # Copy from previous assignment
        green = pygame.Color("green")

        for i in range(self.life.rows):
            y = i * self.cell_size
            for j in range(self.life.cols):
                if self.life.curr_generation[i][j]:
                    x = j * self.cell_size
                    pygame.draw.rect(self.screen, green, (x, y, self.cell_size, self.cell_size))

    def _handle_events(self) -> None:
        """Обработка событий PyGame."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)
            elif event.type == pygame.MOUSEBUTTONDOWN and self.paused:
                self._handle_mouse_click(event)

    def _handle_keydown(self, event: pygame.event.Event) -> None:
        """Обработка нажатий клавиш."""
        if event.key == pygame.K_SPACE:
            self.paused = not self.paused

    def _handle_mouse_click(self, event: pygame.event.Event) -> None:
        """Обработка кликов мыши на паузе."""
        x, y = event.pos
        row = y // self.cell_size
        col = x // self.cell_size

        # Проверяем границы и переключаем клетку
        if 0 <= row < self.life.rows and 0 <= col < self.life.cols:
            # Переключаем состояние клетки
            self.life.curr_generation[row][col] = 1 - self.life.curr_generation[row][col]

    def _update(self) -> None:
        """Обновление состояния игры."""
        if not self.paused and not self.life.is_max_generations_exceeded:
            self.life.step()

    def _draw_ui(self) -> None:
        """Отрисовка пользовательского интерфейса."""
        font = pygame.font.Font(None, 36)

        # Поколение
        text = font.render(f"Поколение: {self.life.generations}", True, (0, 0, 0))
        self.screen.blit(text, (10, 10))

        # Статус паузы
        if self.paused:
            text = font.render("ПАУЗА", True, (255, 0, 0))
            self.screen.blit(text, (10, 50))

    def run(self) -> None:
        # Copy from previous assignment
        while self.running:
            self._handle_events()
            self._update()

            # Отрисовка
            self.screen.fill(pygame.Color("white"))
            self.draw_grid()
            self.draw_lines()
            self._draw_ui()

            pygame.display.flip()
            self.clock.tick(self.speed)

        pygame.quit()


if __name__ == "__main__":
    life = GameOfLife(size=(20, 30), randomize=True, max_generations=100)
    gui = GUI(life, cell_size=20, speed=10)
    gui.run()
