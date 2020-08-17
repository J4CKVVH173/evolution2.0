import settings
import copy
import random

from typing import List
from tkinter import Tk, Canvas

from cells import Empty, Wall, BaseCell, PlantFood


class Window:
    """Класс Абстракция для отрисовки окна и сетки мира."""

    TITLE = "Evolution"
    WIDTH = 1280
    HEIGHT = 720
    BACKGROUND = "yellow"

    def __init__(self):
        self._root = Tk()
        self._root.title(self.TITLE)
        self._root.geometry(f"{self.WIDTH}x{self.HEIGHT}")

        self._canvas = Canvas(self._root, width=self.WIDTH, height=self.HEIGHT, background=self.BACKGROUND)
        self._canvas.pack()

    def mainloop(self):
        """Метод для запуска основного цикла, который необходим для отрисовки окна."""
        self._root.mainloop()

    def create_rectangle(self, x1: int, y1: int, x2: int, y2: int, fill: str = settings.EMPTY) -> int:
        """Метод для генерации прямоугольника.

        Args:
            x1 (int): Координате левого верхнего угла по x
            y1 (int): Координата левого верхнего угла по y
            x2 (int): Координата нижнего правого угла по x
            y2 (int): Координата нижнего правого угла по y
            fill (str, optional): Цвет, которым будет залит прямоугольник. Defaults to settings.EMPTY.

        Returns:
            int: Будет возвращен id, под которым создан элемент.
        """
        item_id = self._canvas.create_rectangle(x1, y1, x2, y2, fill=fill)
        return item_id

    def update(self):
        self._canvas.update()

    def change_cell_color(self, cell_id, fill):
        self._canvas.itemconfig(cell_id, fill=fill)


class World:
    """Класс Реализация для управления миром, в котором существуют клетки."""

    GRID = [
        [-1] * settings.COL for g in range(settings.ROW)
    ]  # представление мира ввиде матрицы, все манипуляции с миром сперва делаются с матрицей

    def __init__(self, window: Window):
        self._window = window
        self._generate_map()
        self._generate_walls()
        self._set_food(150)

    def _generate_map(self):
        """Метод вызывается для первичной генерации мира, заполняет его пустыми клетками."""
        y1 = 0
        y2 = settings.CELL_Y
        for i, row in enumerate(self.GRID):
            x1 = 0
            x2 = settings.CELL_X
            for j, cell in enumerate(row):
                empty = Empty()
                id = self._window.create_rectangle(x1, y1, x2, y2)
                empty.set_id(id)
                self.GRID[i][j] = empty
                x1 += settings.CELL_X
                x2 += settings.CELL_X
            y1 += settings.CELL_Y
            y2 += settings.CELL_Y

    def _generate_walls(self):
        """Метод для первичного вызова, генерирует в пустом мире стены, за пределы которого клекти не могут выйти."""
        new_grid = copy.deepcopy(self.GRID)
        first_row = new_grid[0]
        last_row = new_grid[-1]

        def _fill_row(Cell: BaseCell, row: List[BaseCell], row_index: int) -> None:
            for i, cell in enumerate(row):
                new_cell = Cell()
                new_cell.set_id(cell.get_id)
                new_grid[row_index][i] = new_cell

        _fill_row(Wall, first_row, 0)
        _fill_row(Wall, last_row, -1)

        self._update_world(new_grid)

    def _update_world(self, new_world: List[List[BaseCell]]):
        for i, row in enumerate(self.GRID):
            if not row == new_world[i]:
                for j, cell in enumerate(row):
                    if not cell == new_world[i][j]:
                        self._window.change_cell_color(new_world[i][j].get_id, new_world[i][j].get_color)
        self.GRID = copy.deepcopy(new_world)

    def _set_food(self, count: int) -> None:
        """Метод генерирует определенное количество еды в мире в рандомных пустых местах."""
        new_grid = copy.deepcopy(self.GRID)

        coefficient = 0.1
        if count < 100:
            coefficient /= 10

        print(coefficient)

        while True:
            for i, row in enumerate(new_grid):
                for j, cell in enumerate(row):
                    if not cell.is_solid:
                        # из-за низкой вероятности создания клетки растительной пищи и бесконечного цикла, достигается
                        # равномерное покрытие
                        if random.random() < coefficient:
                            food = PlantFood()
                            food.set_id(cell.get_id)
                            new_grid[i][j] = food

                            count -= 1

                            if count == 0:
                                self._update_world(new_grid)
                                return

    def execute(self):
        while True:
            self._window.update()
