from abc import ABC, abstractmethod

from typing import Tuple

from cells import BaseCell
from action.arbiter_handler import StartMove, Move, EatHerbFood


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
        start = StartMove()
        move = Move()
        eat = EatHerbFood()

        start.set_next(move)
        move.set_next(eat)

        start.handle(cell, coordinates, old_map, new_map)

        cell.reset_move_info()
