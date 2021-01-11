import settings

from cells.base import BaseCell


class EmptyType:
    """Внешнее состояние пустой ячейки."""

    COLOR = settings.EMPTY
    HEALTH = -1


class Empty(BaseCell):
    """Легковес пустой ячейки, из которых по умолчанию состоит мир."""

    TYPE = EmptyType()

    def __init__(self):
        super().__init__()
        self.SOLID = False
        self.COST = 0.0

    @property
    def get_color(self):
        return self.TYPE.COLOR

    def busy(self):
        self.SOLID = True
