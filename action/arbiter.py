from abc import ABC, abstractmethod

from typing import Tuple

from cells import Empty, BaseCell


class ActionContext:
    """Контекст для стратегий взаимодействия с миром."""

    _strategy: "Arbiter" = None

    def set_strategy(self, strategy: "Arbiter") -> None:
        """Метод для установки стратегии.

        Args:
            strategy (Arbiter): Объект наследник класса Arbiter который будет установлен в качестве стратегии в контекст
            исполнения.
        """
        self._strategy = strategy

    def execute(
        self,
        cell: BaseCell,
        coordinates: Tuple[int, int],
        old_map: Tuple[Tuple[BaseCell]],
        new_map: Tuple[Tuple[BaseCell]],
    ):
        """Метод для исполнения метода стратегии.

        Args:
            cell (BaseCell): Ячейка к которой будет применяться стратегия
            coordinates: Tuple[int, int]: Координаты текущего местоположения клетки
            old_map (Tuple[Tuple[BaseCell]]): Старое матриченое представление карты
            new_map (TupleTuple[Tuple[BaseCell]]): Новое матричное представление карты
        """
        self._strategy.cell_move(cell, coordinates, old_map, new_map)


class Arbiter(ABC):
    """Класс предоставляющий общией интерфейс для стратегий, отвечающих за взаимодействие клеток с миром."""

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance

    @abstractmethod
    def cell_move(
        self,
        cell: BaseCell,
        coordinates: Tuple[int, int],
        old_map: Tuple[Tuple[BaseCell]],
        new_map: Tuple[Tuple[BaseCell]],
    ):
        """Метод отвечающий за логику перемещения клетки в мире.

        Args:
            cell (BaseCell): Ячейка к которой будет применяться стратегия
            coordinates: Tuple[int, int]: Координаты текущего местоположения клетки
            old_map (Tuple[Tuple[BaseCell]]): Старое матриченое представление карты
            new_map (Tuple[Tuple[BaseCell]]): Новое матричное представление карты
        """
        pass


class HerbArbiter(Arbiter):
    """Класс стратегия, отвечающий за движение травоядных клеток в мире."""

    def cell_move(
        self,
        cell: BaseCell,
        coordinates: Tuple[int, int],
        old_map: Tuple[Tuple[BaseCell]],
        new_map: Tuple[Tuple[BaseCell]],
    ):
        action = cell.get_move_info()
        # ToDo реализовать как цепочку
        move = action.get_move()
        if move is not None:
            x_delta, y_delta = move
            x, y = coordinates
            map_width = len(old_map[0])
            map_height = len(old_map)

            j = x + x_delta  # высчитывается новая координата положения

            # выставляем положение с другого конца (мир замкнут по кругу)
            if j >= map_width:
                j -= map_width
            if j < 0:
                j += map_width

            i = y + y_delta

            if i >= map_height:
                i -= map_height
            if i < 0:
                i += map_height

            new_position_cell = old_map[i][j]
            if not new_position_cell.is_solid:
                new_position_cell.busy()
                new_map[y][x] = Empty().set_id(cell.get_id)
                new_map[i][j] = cell.set_id(new_position_cell.get_id)
