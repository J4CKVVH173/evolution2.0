import settings

from action.move import Move, MoveBuilder
from cells.base import BaseCell


class Herbivore(BaseCell):
    """Класс травоядной ячейки."""
    # ToDo сделать общий класс для травоядных клеток и для хищных.

    COLOR = settings.CELL_HERBIVORE
    HEALTH = 50
    SOLID = True
    FIXED = False

    GENOME = [3, 3, 3, 3, 2, 2, 1, 1, 2, 2]
    GENOME_POINTER = 0

    def __init__(self):
        self._move_info = MoveBuilder()

    def set_state(self):
        pass

    def make_move(self) -> None:
        gen = self.get_gen()
        if gen == 1:
            self._move_info.set_move_y(-1)  # вверх
        if gen == 2:
            self._move_info.set_move_x(1)  # вправо
        if gen == 3:
            self._move_info.set_move_y(1)  # вниз
        if gen == 4:
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

    @property
    def get_color(self):
        return self.COLOR

    @property
    def is_solid(self):
        return self.SOLID
