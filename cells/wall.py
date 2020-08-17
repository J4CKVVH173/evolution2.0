import settings

from cells.base import BaseCell


class WallType:
    """Внешнее состояние ячейки стены."""

    COLOR = settings.WALL
    HEALTH = -1
    SOLID = True


wall_type = WallType()


class Wall(BaseCell):
    """Легковес ячейки стены."""

    TYPE = wall_type

    def make_move(self):
        pass

    def set_state(self):
        pass

    @property
    def get_color(self):
        return self.TYPE.COLOR

    @property
    def is_solid(self):
        return self.TYPE.SOLID

    def __repr__(self):
        return f'Wall: {self.MAP_ID}'
