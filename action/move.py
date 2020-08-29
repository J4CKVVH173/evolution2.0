from typing import Tuple, Union


class Move:
    """Класс содержит информацию о сделанном шаге клетке."""

    def __init__(self, x: int = None, y: int = None, bite: bool = False):
        self.MOVE_X = x
        self.MOVE_Y = y
        self.BITE = bite

    def get_move(self) -> Union[Tuple[int, int], None]:
        """Метод возвращает информацию о том, куда клетка делает шаг.

        Returns:
            Union[Tuple[int], None]: Информация о сделанном шаге клетко, если клетка не двигается, возвращается None.
        """
        # Если клетка кусает, она не ходит
        if self.BITE:
            return None
        return self.MOVE_X, self.MOVE_Y

    def get_bite(self) -> Union[Tuple[int, int], None]:
        """Метод возвращает информацию о том, куда клетка кусает.

        Returns:
            Union[Tuple[int, int], None]: Информация об укусе, если клетка не кусает, возвращается None.
        """
        if not self.BITE:
            return None
        return self.MOVE_X, self.MOVE_Y


class MoveBuilder:
    def __init__(self):
        self.reset()

    def reset(self):
        """Метод для сброса значений в дефолтное состояние."""
        self._X = 0
        self._Y = 0
        self._BITE = False

    def set_move_x(self, x: int) -> None:
        """Метод устанавливает значение для шага по оси X.

        Args:
            x (int): Значение для шага по оси X.
        """
        self._X += x

    def set_move_y(self, y: int) -> None:
        """Метод устанавливает значение для шага по оси Y.

        Args:
            x (int): Значение для шага по оси Y.
        """
        self._Y += y

    def build(self) -> Move:
        product = Move(self._X, self._Y, self._BITE)
        return product
