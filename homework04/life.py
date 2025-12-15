import pathlib
import random
import typing as tp

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        # Copy from previous assignment
        if randomize:
            return [[random.randint(0, 1) for _ in range(self.cols)] for _ in range(self.rows)]
        return [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def get_neighbours(self, cell: Cell) -> Cells:
        # Copy from previous assignment
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
                if 0 <= neighbor_row < self.rows and 0 <= neighbor_col < self.cols:
                    neighbours.append(self.curr_generation[neighbor_row][neighbor_col])

        return neighbours

    def get_next_generation(self) -> Grid:
        # Copy from previous assignment
        new_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        for y in range(self.rows):
            for x in range(self.cols):
                neighbours = self.get_neighbours((y, x))
                alive_neighbours = sum(neighbours)

                # Применяем правила игры "Жизнь"
                if self.curr_generation[y][x]:  # Живая клетка
                    if 2 <= alive_neighbours <= 3:
                        new_grid[y][x] = 1
                else:  # Мёртвая клетка
                    if alive_neighbours == 3:
                        new_grid[y][x] = 1

        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = [row[:] for row in self.curr_generation]
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations is None:
            return False
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, "r") as f:
            lines = [line.strip() for line in f if line.strip()]

        # Определяем размеры сетки
        rows = len(lines)
        cols = len(lines[0]) if rows > 0 else 0

        # Создаем сетку из файла
        grid = []
        for line in lines:
            if len(line) != cols:
                raise ValueError("Все строки в файле должны быть одинаковой длины")
            row = [int(char) for char in line]
            grid.append(row)

        # Создаем экземпляр GameOfLife
        game = GameOfLife(size=(rows, cols), randomize=False, max_generations=float("inf"))
        game.curr_generation = grid
        game.prev_generation = [[0] * cols for _ in range(rows)]

        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w") as f:
            for row in self.curr_generation:
                line = "".join(str(cell) for cell in row)
                f.write(line + "\n")
