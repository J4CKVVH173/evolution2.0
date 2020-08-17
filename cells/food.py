import settings

from cells.base import BaseCell


class PlantFood(BaseCell):

    COLOR = settings.PLANT_FOOD
    HEALTH = 1
    SOLOD = True

    def set_state(self):
        pass

    def make_move(self):
        pass

    @property
    def get_color(self):
        return self.COLOR
