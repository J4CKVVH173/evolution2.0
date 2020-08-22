import settings

from cells.base import BaseCell


class PlantFood(BaseCell):
    """Класс ячейки растительной еды."""

    COLOR = settings.PLANT_FOOD

    def __init__(self):
        super().__init__()
        self.HEALTH = 1

    @property
    def get_color(self):
        return self.COLOR

    @property
    def can_move(self):
        return False
