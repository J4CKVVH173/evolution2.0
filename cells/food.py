import settings

from cells.base import BaseCell


class Food(BaseCell):
    """Общий класс для реализации клеток пищи."""

    def __init__(self):
        super().__init__()
        self.HEALTH = 1
        self.COST = 0.5

    def eat(self) -> None:
        """Метод для поедания клетки."""
        self.HEALTH = 0

    @property
    def get_cost(self) -> None:
        if self.can_eat:
            return self.COST
        return self.NOT_ACTIVE_COST

    @property
    def can_eat(self) -> bool:
        """Метод для проверки, можно ли съесть клетку.

        Returns:
            bool: True - если клетка съедобная и False если клетка не съедобная
        """
        return self.HEALTH > 0


class PlantFood(Food):
    """Класс ячейки растительной еды."""

    COLOR = settings.PLANT_FOOD

    @property
    def get_color(self):
        return self.COLOR
