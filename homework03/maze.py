from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


# Сетка лабиринта из стенок


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    """
    Удаляет стену в направлении up или right
    """
    x, y = coord
    cols = len(grid[0])
    direction = choice(("up", "right"))

    if direction == "up":
        if x > 1:
            grid[x - 1][y] = " "
        elif y < cols - 2:
            grid[x][y + 1] = " "
    else:
        if y < cols - 2:
            grid[x][y + 1] = " "
        elif x > 1:
            grid[x - 1][y] = " "

    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    """
    Генерация лабиринта бинарным деревом
    """
    grid = create_grid(rows, cols)
    empty_cells = []

    # Создаем пустоты, от которых будем строить пути
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    # Удаляем стены между пустотами
    for cell in empty_cells:
        remove_wall(grid, cell)

    # Создаем вход и выход(фикс вход слева вверху)
    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in {0, rows - 1} else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in {0, rows - 1} else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"
    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """
    Находит координаты входов/выходов в лабиринте - 2шт
    """
    exits = []
    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if cell == "X":
                exits.append((x, y))
                if len(exits) == 2:
                    return exits
    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """
    Куда можно походить - нумерует возможные шаги
    """
    rows, cols = len(grid), len(grid[0])
    # размер сетки
    for x in range(rows):
        for y in range(cols):
            if grid[x][y] == k:
                # Проверяем соседей во все стороны
                neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
                for nx, ny in neighbors:
                    if 0 <= nx < rows and 0 <= ny < cols:
                        if grid[nx][ny] == 0:
                            grid[nx][ny] = k + 1
    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """
    Восстанавливает кратчайший путь по пронумерованной сетке - каким именно путем пойдем
    """
    rows, cols = len(grid), len(grid[0])
    x, y = exit_coord
    k = int(grid[x][y])
    path = [(x, y)]

    while k > 1:
        k -= 1
        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        for nx, ny in neighbors:
            if 0 <= nx < rows and 0 <= ny < cols:
                if grid[nx][ny] == k:
                    path.append((nx, ny))
                    x, y = nx, ny
                    break
    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """
    Проверяет, не заблокирован ли выход стенами
    """
    rows, cols = len(grid), len(grid[0])
    x, y = coord

    # Угловые клетки всегда заблокированы
    if (x == 0 or x == rows - 1) and (y == 0 or y == cols - 1):
        return True
    # Проверяем соседей для клеток на границе
    if x == 0 and grid[x + 1][y] != " ":
        return True
    if x == rows - 1 and grid[x - 1][y] != " ":
        return True
    if y == 0 and grid[x][y + 1] != " ":
        return True
    if y == cols - 1 and grid[x][y - 1] != " ":
        return True

    return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """
    Решает лабиринт с помощью волнового алгоритма - намечаем путь
    """
    grid = deepcopy(grid)
    exits = get_exits(grid)

    # 1 вход и 1 выход, не заблокированы
    if len(exits) != 2:
        return grid, None

    for exit_coord in exits:
        if encircled_exit(grid, exit_coord):
            return grid, None

    # Вход 1, остальное 0
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == " ":
                grid[x][y] = 0

    start_x, start_y = exits[0]
    exit_x, exit_y = exits[1]

    grid[start_x][start_y] = 1
    grid[exit_x][exit_y] = 0

    # Распространение волны
    k = 1
    max_iterations = len(grid) * len(grid[0])

    while grid[exit_x][exit_y] == 0 and k < max_iterations:
        grid = make_step(grid, k)
        k += 1

    # Если выход не достигнут
    if grid[exit_x][exit_y] == 0:
        return grid, None

    # Восстанавливаем путь
    path = shortest_path(grid, (exit_x, exit_y))
    return grid, path


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """
    Рисует путь в лабиринте
    """
    # Путь есть, он список - пройдемся и поставим крестики
    if path and isinstance(path, list):
        for x, y in path:
            grid[x][y] = "X"
    return grid


if __name__ == "__main__":
    print("Сгенерированный лабиринт:")
    print(pd.DataFrame(bin_tree_maze(15, 15)))

    print("\nРешение лабиринта:")
    GRID = bin_tree_maze(15, 15)
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
