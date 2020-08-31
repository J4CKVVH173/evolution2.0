import random
from abc import abstractmethod

from action.move import Move, MoveBuilder
from cells.base import BaseCell


class BaseLive(BaseCell):
    """Базовый класс для живых клеток."""

    def __init__(self, genom=None, health=30):
        super().__init__()
        self.GENOME = []
        self.GENOME_POINTER = 0
        self.HEALTH = health
        self.FIXED = False

        self._move_info = MoveBuilder()

        if genom:
            self._set_genom(genom)
        else:
            self._generate_genome()

    @abstractmethod
    def got_food(self):
        """Метод для установки внутреннего состояния клетки, после того как клетка поела."""
        pass

    @abstractmethod
    def make_move(self):
        """Метод для совершения шага клеткой."""
        pass

    def get_gen(self) -> int:
        """Метод для получения гена на текущий ход.

        Returns:
            int: Ген на текущий ход.
        """
        gen = self.GENOME[self.GENOME_POINTER]
        self.GENOME_POINTER += 1
        if len(self.GENOME) == self.GENOME_POINTER:
            self.GENOME_POINTER = 0

        return gen

    def _generate_genome(self) -> None:
        """Метод для генерации первоначального генома."""
        for _ in range(64):
            self.GENOME.append(random.randint(0, 35))

    def _set_genom(self, genom: list) -> None:
        """Метод для установки генома.

        Args:
            genom (list): Геном который будет установлен клетке.
        """
        self.GENOME = genom.copy()

    def get_move_info(self) -> Move:
        """Метод формирует объект класса Move с информацией о движении клеток и возвращает его.

        Returns:
            Move: Объект класса Move.
        """
        return self._move_info.build()

    def reset_move_info(self) -> None:
        """Метод производит сброс настроек об информации движения клетки."""
        self._move_info.reset()

    def save_genom(self) -> list:
        """Метод для сохранение существующего генома клетки.

        Returns:
            list: Геном клетки.
        """
        return self.GENOME.copy()

    def _change_health(self, count: int = -1):
        """Метод для изменения здоровья клетки.

        Args:
            count (int, optional): Значение на которое здоровье клетки должно быть уменьшено. Defaults to -1.
        """
        self.HEALTH += count

    def reprodaction(self) -> 'BaseLive':
        """Интерфейс прототипа для создания копии клетки.

        Returns:
            BaseLive: Будет возвращена копия клетки.
        """
        pass

    @property
    def get_color(self) -> str:
        return self.COLOR

    @staticmethod
    @property
    def can_reproduction(self):
        """Свойство определяет, может ли клетка размножаться или нет."""
        pass

    @property
    def is_dead(self) -> bool:
        """Свойство возвращает информацию о том, жива ли клетка.

        Если здоровье клетки 0 или меньше, то она считается мертвой.
        Returns:
            bool: True - если мертва, False - если жива
        """
        return self.HEALTH <= 0
