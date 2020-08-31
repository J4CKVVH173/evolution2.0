from typing import Tuple, Union


class Move:
    """Класс содержит информацию о сделанном шаге клетке."""

    def __init__(self, x: int = None, y: int = None, bite: bool = False, reproduction=False):
        self.MOVE_X = x
        self.MOVE_Y = y
        self.BITE = bite
        self.REPRODUCTION = reproduction

    def get_move(self) -> Union[Tuple[int, int], None]:
        """Метод возвращает информацию о том, куда клетка делает шаг.

        Returns:
            Union[Tuple[int], None]: Информация о сделанном шаге клетко, если клетка не двигается, возвращается None.
        """
        # Если клетка кусает, она не ходит
        if self.BITE or self.REPRODUCTION:
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

    def is_reproduction(self) -> bool:
        """Метод возвращает информацию о том, производит ли клетка деление.

        Returns:
            bool: True - если клетка производит деление, False если нет
        """
        return self.REPRODUCTION


class MoveBuilder:
    def __init__(self):
        self.reset()

    def reset(self):
        """Метод для сброса значений в дефолтное состояние."""
        self._X = 0
        self._Y = 0
        self._BITE = False
        self._REPRODUCTION = False

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

    def set_bite(self, bite=True) -> None:
        """Метод устанавливает значение укуса.

        Args:
            bite (bool, optional): True если клетка кусает. Defaults to True.
        """
        self._BITE = bite

    def set_reproduction(self, reproduction: bool = True) -> None:
        """Метод устанавливает значения размножения.

        Args:
            reproduction (bool): True если клетка производит размножение.
        """
        self._REPRODUCTION = reproduction

    def build(self) -> Move:
        product = Move(self._X, self._Y, self._BITE, self._REPRODUCTION)
        return product
