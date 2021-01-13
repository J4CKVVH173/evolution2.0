import copy
import random
import time
from tkinter import Button, Canvas, Tk
from typing import List

import settings
from action import ActionContext, HerbArbiter
from cells import BaseCell, Empty, PlantFood, Wall
from cells.live.herbivore import Herbivore
from cells.reproduction import Reprodaction
from lib.population import Grave, Population
from lib.utils import duck_typing_elements_equals, duck_typing_lists_equals
from logs.logging import Log


class Window:
    """Класс Абстракция для отрисовки окна и сетки мира."""

    TITLE = "Evolution"
    WIDTH = 1280
    HEIGHT = 770
    BACKGROUND = "yellow"

    def __init__(self):
        self._root = Tk()
        self._root.title(self.TITLE)
        self._root.geometry(f"{self.WIDTH}x{self.HEIGHT}")

        Button(self._root, text="exit", bg="black", fg="white", command=self._exit_command).place(x=1200, y=0)
        self.pause_button = Button(self._root, text="pause", bg="black", fg="white")
        self.pause_button.place(x=0, y=0)
        self.resume_button = Button(self._root, text="resume", bg="black", fg="white")
        self.resume_button.place(x=70, y=0)
        self.slow_mode = Button(self._root, text="slow", bg="black", fg="white")
        self.slow_mode.place(x=145, y=0)
        self._canvas = Canvas(self._root, width=self.WIDTH, height=self.HEIGHT, background=self.BACKGROUND)
        self._canvas.place(x=0, y=30)

        self.cells_count = self._canvas.create_text(60, 720, text=f"Live cells: {settings.CELLS_POPULATION}")
        self.epoch_count = self._canvas.create_text(160, 720, text="Epoch: 1")
        self.steps_count = self._canvas.create_text(280, 720, text="Steps: 1")
        self.past_steps_count = self._canvas.create_text(390, 720, text="Past steps: 0")

    def _exit_command(self):
        self._root.destroy()

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

    def change_cells_count(self, count: int) -> None:
        """Метод производит обновление текста, отображающего количество живых клеток в мире.

        Args:
            count (int): Число живых клеток.
        """
        self._canvas.itemconfig(self.cells_count, text=f"Live cells: {count}")

    def change_steps_count(self, count: int) -> None:
        """Метод производит обновление текста, отображающего число количества шагов.

        Args:
            count (int): Число шагов в эпохе
        """
        self._canvas.itemconfig(self.steps_count, text=f"Steps: {count}")

    def change_epoch_count(self, count: int) -> None:
        """Метод производит обновление текста, отображающего текущую эпоху.

        Args:
            count (int): Число шагов в эпохе
        """
        self._canvas.itemconfig(self.epoch_count, text=f"Epoch: {count}")

    def change_past_steps_count(self, count: int) -> None:
        """Метод производит обновление текста, отображающее количество шагов в предыдущей эпохе.

        Args:
            count (int): Число шагов в предыдущей эпохе.
        """
        self._canvas.itemconfig(self.past_steps_count, text=f"Past steps: {count}")

    def set_pause_command(self, command):
        """Метод производит установку команды для кнопки паузы.

        Args:
            command (callback): Функция которая будет установлена в кнопку.
        """
        self.pause_button.configure(command=command)

    def set_resume_command(self, command):
        """Метод производит установку команды для кнопки продолжить.

        Args:
            command (callback): Функция которая будет установлена в кнопку.
        """
        self.resume_button.configure(command=command)

    def set_slowmode_command(self, command):
        """Метод производит установку команды для кнопки замедленного режима.

        Args:
            command (callback): Функция которая будет установлена в кнопку.
        """
        self.slow_mode.configure(command=command)


class World:
    """Класс Реализация для управления миром, в котором существуют клетки."""

    GRID = [
        [-1] * settings.COL for g in range(settings.ROW)
    ]  # представление мира в виде матрицы, все манипуляции с миром сперва делаются с матрицей

    def __init__(self, window: Window):
        self._window = window
        self._bind_buttons()
        self.population = Population(settings.CELLS_POPULATION)
        self.grave = Grave()
        self.reproduction = Reprodaction()
        self.epoch = 1
        self.step = 1
        self.sleep_time = 0

        self._subscribe()

        self._action_context = ActionContext()
        self._herb_arbiter = HerbArbiter()

        self._generate_map()
        self._generate_walls()
        self._set_cells(PlantFood, 150)
        self._set_cells(Herbivore, settings.CELLS_POPULATION)

        self.is_active_world = True

    def _bind_buttons(self):
        """Метод производит прикрепление методов к кнопкам."""
        self._window.set_pause_command(self.stop_world)
        self._window.set_resume_command(self.resume_world)
        self._window.set_slowmode_command(self.change_sleep_time)

    def _subscribe(self):
        """Производим подписку на объекты травоядных клеток."""
        Herbivore.add_born_sub(self.population)
        Herbivore.add_death_sub(self.population)
        Herbivore.add_death_sub(self.grave)

    def _generate_map(self):
        """Метод вызывается для первичной генерации мира, заполняет его пустыми клетками."""
        y1 = 0
        y2 = settings.CELL_Y
        for i, row in enumerate(self.GRID):
            x1 = 0
            x2 = settings.CELL_X
            for j, _ in enumerate(row):
                empty = Empty()
                map_id = self._window.create_rectangle(x1, y1, x2, y2)
                empty.set_id(map_id)
                self.GRID[i][j] = empty
                x1 += settings.CELL_X
                x2 += settings.CELL_X
            y1 += settings.CELL_Y
            y2 += settings.CELL_Y

    def _generate_walls(self):
        """Метод для первичного вызова, генерирует в пустом мире стены, за пределы которого клетки не могут выйти."""
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

    def _remove_all_cells(self):
        """Метод приводит мир к чистому состоянию."""
        new_grid = copy.deepcopy(self.GRID)

        for i, row in enumerate(new_grid):
            for j, cell in enumerate(row):
                empty = Empty()
                empty.set_id(cell.get_id)
                new_grid[i][j] = empty

        self._update_world(new_grid)

    def _set_cells(self, Cell: BaseCell, count: int, **kwargs) -> None:
        """Метод генерирует определенное количество клеток в мире в рандомные, пустых местах.

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
                            new_cell = Cell(**kwargs)
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
                    cells_around = self._get_round_cost(i, j)
                    cells_around.append(cell.get_health / 100)
                    # сперва клетка делает действие и затем арбитер с учетом типа клетки изменяет внешнее состояние мира
                    cell.make_move(cells_around)
                    if isinstance(cell, Herbivore):
                        self._action_context.set_strategy(self._herb_arbiter)
                    self._action_context.execute(cell, [j, i], self.GRID, new_grid)

        if self.is_end_epoch():
            self.reload_world()
        else:
            self._update_world(new_grid)

        self._update_helpfull_text()

    def _update_helpfull_text(self):
        """Метод для обновления вспомогательного текста."""
        self.step += 1
        self._window.change_steps_count(self.step)
        self._window.change_epoch_count(self.epoch)

    def is_end_epoch(self) -> bool:
        """Метод проверяет, является ли данная итерация концом эпохи."""
        return self.population.total_count == 0

    def _clear_world(self) -> None:
        """Метод для полной очистки мира."""
        self._remove_all_cells()
        self._generate_walls()
        self._set_cells(PlantFood, 175)

    def _fill_new_generation(
        self, best_epoch_cells: list[Herbivore], children, best_mutation, second_mutation, children_mutation
    ) -> None:
        """Метод производит заполнение нового мира клетками с новым геномом.

        Args:
            best_epoch_cells (list): Массив содержащий в себе две лучшие клетки предыдущего поколения
            children (matrix): Скрещенный геном двух лучших клеток предыдущего поколения
            best_mutation (matrix): Измененный геном лучшей клетки предыдущего поколения
            second_mutation (matrix): Измененный геном второй лучшей клетки предыдущего поколения
            children_mutation (matrix): Измененный геном ребенка лучших клеток
        """
        best = best_epoch_cells[0]
        second = best_epoch_cells[1]
        self._set_cells(Herbivore, 8, genome=best.save_genome(), clan=best.get_clan_name, color=settings.BEST)
        self._set_cells(Herbivore, 8, genome=second.save_genome(), clan=second.get_clan_name, color=settings.SECOND)
        self._set_cells(Herbivore, 8, genome=children, color=settings.CHILDREN)
        self._set_cells(Herbivore, 8, genome=best_mutation)
        self._set_cells(Herbivore, 8, genome=second_mutation)
        self._set_cells(Herbivore, 8, genome=children_mutation)

    def reload_world(self) -> None:
        """Метод производит перезапуск мира, если был конец эпохи."""
        self._window.change_past_steps_count(self.step)

        self._clear_world()

        best_epoch_cells = self.grave.get_best()
        children_genome = self.reproduction.crossing(*best_epoch_cells)
        best_genome = best_epoch_cells[0].save_genome()
        second_genome = best_epoch_cells[1].save_genome()

        Log.log_genome(best_epoch_cells, self.epoch)
        Log.log_info(self.epoch, self.step)

        self.epoch += 1
        self.step = 0

        best_mutated_genome = list()
        second_mutated_genome = list()
        mutated_children = list()
        for genome in best_genome:
            best_mutated_genome.append(self.reproduction.mutation(genome))
        for genome in second_genome:
            second_mutated_genome.append(self.reproduction.mutation(genome, 0.4))
        for genome in children_genome:
            mutated_children.append(self.reproduction.mutation(genome))

        self._fill_new_generation(
            best_epoch_cells, children_genome, best_mutated_genome, second_mutated_genome, mutated_children
        )
        # обновлять популяцию нужно после того как мир был заново заселен клетками
        self.grave.clear()
        self.population.update_population(self.GRID)

    def _get_round_cost(self, i: int, j: int) -> list:
        """Метод возвращает значения всех клеток вокруг той, что должна совершить движение двигается.

        Args:
            i (int): Расположение клетки совершающей движение по оси y
            j (int): Расположение клетки совершающей движение клетки по оси x

        Returns:
            list: Массив содержащий все веса клеток, окружающие движущуюся, начиная с левого верхнего угла и по часовой.
        """
        # т.к. мир замкнут по горизонтали, смотрим с другой стороны
        if j == 0:
            return [
                self.GRID[i - 1][settings.COL - 1].get_cost,
                self.GRID[i - 1][j].get_cost,
                self.GRID[i - 1][j + 1].get_cost,
                self.GRID[i][settings.COL - 1].get_cost,
                self.GRID[i][j + 1].get_cost,
                self.GRID[i + 1][settings.COL - 1].get_cost,
                self.GRID[i + 1][j].get_cost,
                self.GRID[i + 1][j + 1].get_cost,
            ]
        if j == settings.COL - 1:
            return [
                self.GRID[i - 1][j - 1].get_cost,
                self.GRID[i - 1][j].get_cost,
                self.GRID[i - 1][0].get_cost,
                self.GRID[i][j - 1].get_cost,
                self.GRID[i][0].get_cost,
                self.GRID[i + 1][j - 1].get_cost,
                self.GRID[i + 1][j].get_cost,
                self.GRID[i + 1][0].get_cost,
            ]
        return [
            self.GRID[i - 1][j - 1].get_cost,
            self.GRID[i - 1][j].get_cost,
            self.GRID[i - 1][j + 1].get_cost,
            self.GRID[i][j - 1].get_cost,
            self.GRID[i][j + 1].get_cost,
            self.GRID[i + 1][j - 1].get_cost,
            self.GRID[i + 1][j].get_cost,
            self.GRID[i + 1][j + 1].get_cost,
        ]

    def _update_world(self, new_world: List[List[BaseCell]]):
        """Метод производит перерисовку мира.

        Принимается обновленное состояние мира, сравнивается со старым состоянием, если положение клеток поменялось,
        производится точечная перерисовка, и старое состояние мира заменяется на новое.

        Args:
            new_world (List[List[BaseCell]]): Матрица содержащая обновленное состояние мира, новое положение клеток.
        """
        for i, row in enumerate(self.GRID):
            # оптимизация позволяющая пропускать строки в которых визуально ничего не изменилось
            if not duck_typing_lists_equals(row, new_world[i]):
                for j, cell in enumerate(row):
                    # оптимизация позволяющая пропускать элементы в которых ничего не изменилось
                    if not duck_typing_elements_equals(cell, new_world[i][j]):
                        self._window.change_cell_color(new_world[i][j].get_id, new_world[i][j].get_color)
        self.GRID = copy.deepcopy(new_world)

        self._window.change_cells_count(self.population.total_count)

    def stop_world(self):
        self.is_active_world = False

    def resume_world(self):
        self.is_active_world = True

    def change_sleep_time(self):
        if self.sleep_time == 0:
            self.sleep_time = 0.1
        else:
            self.sleep_time = 0

    def execute(self):
        """Метод запуска мира."""
        while True:
            if self.is_active_world:
                self._make_step()
            self._window.update()
            time.sleep(self.sleep_time)
