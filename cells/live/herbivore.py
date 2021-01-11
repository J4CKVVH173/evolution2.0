from .base import BaseLive


class Herbivore(BaseLive):
    """Класс травоядной ячейки."""

    def make_move(self, inputs: list) -> None:
        move_number = self.neurons.compute(inputs)
        # просто движение
        if move_number == 0:
            self._move_info.set_move_y(-1)  # вверх
        elif move_number == 1:
            self._move_info.set_move_x(1)  # вправо
        elif move_number == 2:
            self._move_info.set_move_y(1)  # вниз
        elif move_number == 3:
            self._move_info.set_move_x(-1)  # влево
        # укус
        elif move_number == 4:
            self._move_info.set_move_y(-1)
            self._move_info.set_bite()
        elif move_number == 5:
            self._move_info.set_move_x(1)
            self._move_info.set_bite()
        elif move_number == 6:
            self._move_info.set_move_y(1)
            self._move_info.set_bite()
        elif move_number == 7:
            self._move_info.set_move_x(-1)
            self._move_info.set_bite()
        elif move_number == 8:
            self._move_info.set_reproduction()

        self._change_health()

    def got_food(self):
        self._change_health(20)

    def reprodaction(self):
        self._change_health(-1 * round(self.HEALTH / 2))
        for sub in self.BORN_SUBSCRIBERS:
            sub.new_cell()

        return Herbivore(self.save_genome(), self.get_health, self.get_clan_name)

    @property
    def can_reproduction(self):
        return self.HEALTH > 4
