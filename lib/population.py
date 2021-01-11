from cells.live.base import BaseLive


class Population:
    """Класс представляющий число всей популяции клеток в мире и позволяющий следить за популяцией."""

    def __init__(self, count: int):
        self.total_count = count

    def new_cell(self) -> None:
        """Метод обрабатывающий добавление новой клетки в мир."""
        self.total_count += 1

    def die_cell(self, *args) -> None:
        """Метод обрабатывающий событие смерти клетки в мире и уменьшающий общее число живых клеток."""
        self.total_count -= 1

    @property
    def world_is_extinct(self) -> bool:
        """Метод определяющий, является мир мертвым или нет.

        Returns:
            bool: Если живых клеток не осталось, мир считается мертвым.
        """
        return self.total_count <= 0


class Grave:
    """Класс могила хранит в себе все умершие клетки."""

    def __init__(self):
        self.grave = []

    def die_cell(self, *args) -> None:
        """Общий интерфейс, который вызывается внутри объекта, но который производится подписка."""
        cell: BaseLive = args[0]
        self.grave.append(cell)

    def clear(self) -> None:
        """Метод очищает могилы."""
        self.grave = []

    def get_best(self, uniq_count: int = 2) -> None:
        """Метод производит получение лучших уникальных клеток из всех мертвых."""
        bests = [self.grave.pop()]

        while len(bests) < uniq_count:
            dead_cell = self.grave.pop()
            if dead_cell.get_clan_name != bests[0].get_clan_name:
                bests.append(dead_cell)

        return bests.copy()
