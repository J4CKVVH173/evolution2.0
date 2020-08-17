import settings

from cells.base import BaseCell


class EmptyType:
    """Внешнее состояние пустой ячейки."""

    COLOR = settings.EMPTY
    HEALTH = -1
    SOLID = False


empty_type = EmptyType()


class Empty(BaseCell):
    """Легковес пустой ячейки."""

    TYPE = empty_type

    def make_move(self):
        pass

    def set_state(self):
        pass

    @property
    def get_color(self):
        return self.TYPE.COLOR

    def __repr__(self):
        return f'Empty: {self.MAP_ID}'
