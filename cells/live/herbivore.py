import settings
import random

from action.move import Move, MoveBuilder
from cells.base import BaseCell


class Herbivore(BaseCell):
    """Класс травоядной ячейки."""
    # ToDo сделать общий класс для травоядных клеток и для хищных.

    COLOR = settings.CELL_HERBIVORE
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

    def set_state(self):
        pass

    def make_move(self) -> None:
        gen = self.get_gen()
        if gen in [0, 1, 2, 3]:
            self._move_info.set_move_y(-1)  # вверх
        if gen in [4, 5, 6, 7]:
            self._move_info.set_move_x(1)  # вправо
        if gen in [8, 9, 10, 11]:
            self._move_info.set_move_y(1)  # вниз
        if gen in [12, 13, 14, 15]:
            self._move_info.set_move_x(-1)  # влево

    def get_move_info(self) -> Move:
        return self._move_info.build()

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

    def _set_genom(self, genom: list) -> None:
        """Метод для установки генома.

        Args:
            genom (list): Геном который будет установлен клетке.
        """
        self.GENOME = genom

    def save_genom(self) -> list:
        return self.GENOME.copy()

    @property
    def get_color(self):
        return self.COLOR

    @property
    def is_solid(self):
        return self.SOLID
