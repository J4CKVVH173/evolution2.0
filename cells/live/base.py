import random

from action.move import Move, MoveBuilder
from cells.base import BaseCell


class BaseLive(BaseCell):
    HEALTH = 50
    SOLID = True
    FIXED = False

    GENOME = []
    GENOME_POINTER = 0

    def __init__(self, genom=None):
        self._move_info = MoveBuilder()
        if genom:
            self._set_genom(genom)
        else:
            self._generate_genome()

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
        for i in range(64):
            self.GENOME.append(random.randint(0, 15))

    def set_state(self):
        pass

    def _set_genom(self, genom: list) -> None:
        """Метод для установки генома.

        Args:
            genom (list): Геном который будет установлен клетке.
        """
        self.GENOME = genom

    def get_move_info(self) -> Move:
        """Метод формирует объект класса Move с информацией о движении клеток и возвращает его.

        Returns:
            Move: Объект класса Move.
        """
        return self._move_info.build()

    def save_genom(self) -> list:
        """Метод для сохранение существующего генома клетки.

        Returns:
            list: Геном клетки.
        """
        return self.GENOME.copy()

    @property
    def get_color(self):
        return self.COLOR

    @property
    def is_solid(self):
        return self.SOLID
