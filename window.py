import settings
import copy
import random
import time

from typing import List
from tkinter import Tk, Canvas

from lib.utils import duck_typing_elements_equals, duck_typing_lists_equals

from cells import Empty, Wall, BaseCell, PlantFood
from cells.live.herbivore import Herbivore
from action import HerbArbiter, ActionContext


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

        self._action_context = ActionContext()
        self._herb_arbiter = HerbArbiter()

        self._generate_map()
        self._generate_walls()
        self._set_cells(PlantFood, 150)
        self._set_cells(Herbivore, 50)

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

    def _set_cells(self, Cell: BaseCell, count: int) -> None:
        """Метод генерирует определенное количество клеток в мире в рандомных, пустых местах.

        Args:
            Cell (BaseCell): класс ячейки которыми будет заполняться мир
            count (int): количество ячеек, которыми нужно заполнить мир
        """
        new_grid = copy.deepcopy(self.GRID)

        coefficient = 0.1
        if count < 100:
            coefficient /= 10

        while True:
            for i, row in enumerate(new_grid):
                for j, cell in enumerate(row):
                    if not cell.is_solid:
                        # из-за низкой вероятности создания клетки растительной пищи и бесконечного цикла, достигается
                        # равномерное покрытие
                        if random.random() < coefficient:
                            new_cell = Cell()
                            new_cell.set_id(cell.get_id)
                            new_grid[i][j] = new_cell

                            count -= 1

                            if count <= 0:
                                self._update_world(new_grid)
                                return

    def _make_step(self):
        """Метод для совершения одной итерации мира."""
        new_grid = copy.deepcopy(self.GRID)

        for i, row in enumerate(self.GRID):
            for j, cell in enumerate(row):
                if cell.can_move:
                    cell.make_move()
                    if isinstance(cell, Herbivore):
                        self._action_context.set_strategy(self._herb_arbiter)
                    self._action_context.execute(cell, [j, i], self.GRID, new_grid)

        self._update_world(new_grid)

    def _update_world(self, new_world: List[List[BaseCell]]):
        """Метод производит перерисовку мира.

        Принимается обновленное состояние мира, сравнивается со старым состоянием, если положение клеток поменялось,
        производится точечная перерисовка, и старое состояние мира заменяется на новое.

        Args:
            new_world (List[List[BaseCell]]): Матрица содержащая обновленное состояние мира, новое положение клеток.
        """
        for i, row in enumerate(self.GRID):
            if not duck_typing_lists_equals(row, new_world[i]):
                for j, cell in enumerate(row):
                    if not duck_typing_elements_equals(cell, new_world[i][j]):
                        self._window.change_cell_color(new_world[i][j].get_id, new_world[i][j].get_color)
        self.GRID = copy.deepcopy(new_world)

    def execute(self):
        """Метод запуска мира."""
        while True:
            self._make_step()
            time.sleep(1)
            self._window.update()
