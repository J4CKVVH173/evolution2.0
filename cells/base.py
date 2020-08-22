from abc import ABC, abstractmethod


class BaseCell(ABC):
    """Абстрактный класс, представляющий собой базовый класс для создания ячеек."""

    def __init__(self):
        self.MAP_ID = None
        self.FIXED = True
        self.SOLID = True

    @property
    @abstractmethod
    def get_color(self):
        """Метод для получения цвета клетки."""
        pass

    @property
    def is_solid(self):
        """Метод, для проверки, является ли объект твердым."""
        return self.SOLID

    @property
    def can_move(self) -> bool:
        """Метод возвращает информацию, может ли клетка ходить."""
        return not self.FIXED

    @property
    def get_id(self) -> int:
        return self.MAP_ID

    def set_id(self, id: int) -> 'BaseCell':
        """Метод установки id ячейки.

        Args:
            id (int): id ячейки.
        """
        self.MAP_ID = id
        return self

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.MAP_ID}"

    def duck_typing(self) -> dict:
        """Метод для проведения утиной типизации.

        Returns:
            dict: Объект на основании которого будет проводиться типизация.
        """
        return {"name": self.__class__.__name__, "map_id": self.MAP_ID}
