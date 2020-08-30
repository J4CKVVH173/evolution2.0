import settings

from .base import BaseLive


class Herbivore(BaseLive):
    """Класс травоядной ячейки."""

    COLOR = settings.CELL_HERBIVORE

    def make_move(self) -> None:
        gen = self.get_gen()
        # просто движение
        if gen in [0, 1, 2, 3]:
            self._move_info.set_move_y(-1)  # вверх
        elif gen in [4, 5, 6, 7]:
            self._move_info.set_move_x(1)  # вправо
        elif gen in [8, 9, 10, 11]:
            self._move_info.set_move_y(1)  # вниз
        elif gen in [12, 13, 14, 15]:
            self._move_info.set_move_x(-1)  # влево
        # укус
        elif gen in [16, 17, 18, 19]:
            self._move_info.set_move_y(-1)
            self._move_info.set_bite()
        elif gen in [20, 21, 22, 23]:
            self._move_info.set_move_x(1)
            self._move_info.set_bite()
        elif gen in [24, 25, 26, 27]:
            self._move_info.set_move_y(1)
            self._move_info.set_bite()
        elif gen in [28, 29, 30, 31]:
            self._move_info.set_move_x(-1)
            self._move_info.set_bite()

        self._change_health()

    def got_food(self):
        self._change_health(50)
