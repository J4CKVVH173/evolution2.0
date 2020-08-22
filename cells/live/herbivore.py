import settings

from .base import BaseLive


class Herbivore(BaseLive):
    """Класс травоядной ячейки."""

    COLOR = settings.CELL_HERBIVORE

    def make_move(self) -> None:
        gen = self.get_gen()
        # ToDo оформить ввиде цепочки мб, подумать
        if gen in [0, 1, 2, 3]:
            self._move_info.set_move_y(-1)  # вверх
        if gen in [4, 5, 6, 7]:
            self._move_info.set_move_x(1)  # вправо
        if gen in [8, 9, 10, 11]:
            self._move_info.set_move_y(1)  # вниз
        if gen in [12, 13, 14, 15]:
            self._move_info.set_move_x(-1)  # влево
