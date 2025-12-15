import random
from typing import List, Tuple
import pygame  # type: ignore

Cell = Tuple[int, int]
Cells = List[int]
Grid = List[List[int]]


class GameOfLife:
    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed
        # Заполнение игрового поля
        self.grid = self.create_grid(randomize=True)

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        if randomize:
            return [[random.randint(0, 1) for _ in range(self.cell_width)] for _ in range(self.cell_height)]
        return [[0 for _ in range(self.cell_width)] for _ in range(self.cell_height)]

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for y in range(self.cell_height):
            for x in range(self.cell_width):
                color = pygame.Color("green") if self.grid[y][x] else pygame.Color("white")
                pygame.draw.rect(
                    self.screen, color, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                )

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        neighbours = []
        row, col = cell

        # Проверяем все 8 соседних клеток
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue  # Пропускаем саму клетку
                neighbor_row = row + i
                neighbor_col = col + j

                # Проверяем границы
                if 0 <= neighbor_row < self.cell_height and 0 <= neighbor_col < self.cell_width:
                    neighbours.append(self.grid[neighbor_row][neighbor_col])

        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        new_grid = [[0 for _ in range(self.cell_width)] for _ in range(self.cell_height)]

        for y in range(self.cell_height):
            for x in range(self.cell_width):
                neighbours = self.get_neighbours((y, x))
                alive_neighbours = sum(neighbours)

                # Применяем правила игры "Жизнь"
                if self.grid[y][x]:  # Живая клетка
                    if 2 <= alive_neighbours <= 3:
                        new_grid[y][x] = 1
                else:  # Мёртвая клетка
                    if alive_neighbours == 3:
                        new_grid[y][x] = 1

        return new_grid

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание начальной сетки
        self.grid = self.create_grid(randomize=True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Отрисовка
            self.draw_grid()
            self.draw_lines()

            # Обновление поколения
            self.grid = self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()


if __name__ == "__main__":
    game = GameOfLife(320, 240, 20)
    game.run()
