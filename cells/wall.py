import settings

from cells.base import BaseCell


class WallType:
    """Внешнее состояние ячейки стены."""

    COLOR = settings.WALL
    HEALTH = -1


class Wall(BaseCell):
    """Легковес ячейки стены, они не обладают никакими свойствами, кроме того что через них нельзя пройти."""

    TYPE = WallType()

    @property
    def get_color(self):
        return self.TYPE.COLOR
