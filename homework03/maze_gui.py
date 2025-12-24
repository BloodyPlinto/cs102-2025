import tkinter as tk
from tkinter import messagebox, ttk
from typing import List, Optional, Tuple, Union

from maze import add_path_to_grid, bin_tree_maze, solve_maze


def draw_cell(x, y, color, size: int = 10):
    x *= size
    y *= size
    x1 = x + size
    y1 = y + size
    canvas.create_rectangle(x, y, x1, y1, fill=color)


def draw_maze(grid: List[List[Union[str, int]]], size: int = 10):
    color_counter = 0

    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if cell == " ":
                color = "White"
            elif cell == "■":
                color = "black"
            elif cell == "X":
                if color_counter % 3 == 0:
                    color = "red"
                elif color_counter % 3 == 1:
                    color = "yellow"
                else:
                    color = "green"
                color_counter += 1
            draw_cell(y, x, color, size)


def show_solution():
    global GRID, GARANTEE
    if GARANTEE:
        maze_with_path = add_path_to_grid(GRID, GARANTEE)
        draw_maze(maze_with_path, CELL_SIZE)
    else:
        tk.messagebox.showinfo("Message", "Something went wrong. Restart, please")


def generate_maze_with_path(rows: int, cols: int) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """
    Генерирует лабиринт с гарантированным путем от входа к выходу
    Сначала 3 попытки со случайными выходами, затем с фиксированными
    """
    for _ in range(3):
        maze = bin_tree_maze(rows, cols, random_exit=True)
        _, path = solve_maze(maze)
        if path:
            return maze, path

    while True:
        maze = bin_tree_maze(rows, cols, random_exit=False)
        _, path = solve_maze(maze)
        if path:
            return maze, path


if __name__ == "__main__":
    global GRID, CELL_SIZE, GARANTEE
    N, M = 51, 77

    CELL_SIZE = 10
    GRID, GARANTEE = generate_maze_with_path(N, M)

    window = tk.Tk()
    window.title("Maze")
    window.geometry("%dx%d" % (M * CELL_SIZE + 100, N * CELL_SIZE + 100))

    canvas = tk.Canvas(window, width=M * CELL_SIZE, height=N * CELL_SIZE)
    canvas.pack()

    draw_maze(GRID, CELL_SIZE)
    ttk.Button(window, text="Solve", command=show_solution).pack(pady=20)

    window.mainloop()
