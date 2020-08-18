from abc import ABC, abstractmethod


class BaseCell(ABC):
    """Абстрактный класс, представляющий собой базовый класс для создания ячеек."""

    MAP_ID = None  # ID карты, где находится текущая ячейка

    @abstractmethod
    def set_state(self):
        """Метод для установки внутреннего состояния клетки."""
        pass

    @abstractmethod
    def make_move(self):
        """Метод для совершения клеткой своего действия."""
        pass

    @property
    @abstractmethod
    def get_color(self):
        """Метод для получения цвета клетки."""
        pass

    @property
    @abstractmethod
    def is_solid(self):
        """Метод, для проверки, является ли объект твердым."""
        pass

    @property
    def get_id(self) -> int:
        return self.MAP_ID

    def set_id(self, id: int) -> None:
        """Метод установки id ячейки.

        Args:
            id (int): id ячейки.
        """
        self.MAP_ID = id
