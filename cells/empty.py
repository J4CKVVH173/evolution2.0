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

    @property
    def get_color(self):
        return self.TYPE.COLOR

    @property
    def can_move(self):
        return False

    def busy(self):
        self.SOLID = True
