import settings

from cells.base import BaseCell


class EmptyType:
    """Внешнее состояние пустой ячейки."""

    COLOR = settings.EMPTY
    HEALTH = -1


empty_type = EmptyType()


class Empty(BaseCell):
    """Легковес пустой ячейки, из которых по умолчанию состоит мир."""

    TYPE = empty_type
    SOLID = False

    def make_move(self):
        pass

    def set_state(self):
        pass

    @property
    def get_color(self):
        return self.TYPE.COLOR

    @property
    def is_solid(self):
        return self.SOLID

    @property
    def can_move(self):
        return False

    def busy(self):
        self.SOLID = True
