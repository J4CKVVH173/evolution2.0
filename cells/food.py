import settings

from cells.base import BaseCell


class Food(BaseCell):
    """Общий класс для реализации клеток пищи."""

    def __init__(self):
        super().__init__()
        self.HEALTH = 1

    @property
    def can_move(self):
        return False


class PlantFood(Food):
    """Класс ячейки растительной еды."""

    COLOR = settings.PLANT_FOOD

    def eat(self) -> None:
        """Метод для поедания клетки."""
        self.HEALTH = 0
        self.SOLID = False

    def busy(self) -> None:
        """
        Метод устанавливает клетку закрытой для перемещения на нее.

        После того как клетка была съедена, она становится доступна для того чтобы на ее место могли встать другие
        клетка.
        """
        self.SOLID = True

    @property
    def is_edible(self) -> bool:
        """Метод проеряет, съедобная клетка или нет.

        Returns:
            bool: True - если клетка съедобная и False если клетка не съедобная
        """
        return bool(self.HEALTH)

    @property
    def get_color(self):
        return self.COLOR
