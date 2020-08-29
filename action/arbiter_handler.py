from abc import ABC, abstractmethod

from typing import Tuple

from cells import Empty, BaseCell, PlantFood


class Handler(ABC):
    """Асбтрактный класс для цепочки обработчиков для арбитера."""

    _next: "Handler" = None

    @abstractmethod
    def handle(self) -> bool:
        """Метод для обработки вызова цепочки звена.

        Returns:
            bool: True - если хоть какое то звено цепи обработало вызов, False если никто не обработал вызов.
        """
        pass

    def set_next(self, next: "Handler") -> "Handler":
        """Метод для установки следующей цепочки звена.

        Returns:
            next (Handler): Следующее звено цепочки вызовов.
        """
        self._next = next
        return self


class StartMove(Handler):
    """Звено обработки начало движение клетки, в начале проверяется жива ли клетка чтобы начать действие."""

    def handle(
        self,
        cell: BaseCell,
        coordinates: Tuple[int, int],
        old_map: Tuple[Tuple[BaseCell]],
        new_map: Tuple[Tuple[BaseCell]],
    ):
        x, y = coordinates
        result = False

        if cell.is_dead:
            food = PlantFood().set_id(cell.get_id)
            new_map[y][x] = food
            return True

        if self._next is not None:
            result = self._next.handle(cell, coordinates, old_map, new_map)
        return result


class Move(Handler):
    """Звено обрабатыващее движение клетки."""

    def handle(
        self,
        cell: BaseCell,
        coordinates: Tuple[int, int],
        old_map: Tuple[Tuple[BaseCell]],
        new_map: Tuple[Tuple[BaseCell]],
    ):
        action = cell.get_move_info()
        move = action.get_move()
        x, y = coordinates
        map_width = len(old_map[0])
        map_height = len(old_map)
        result = False

        if move is not None:
            x_delta, y_delta = move
            cell.reset_move_info()

            j = x + x_delta  # высчитывается новая координата положения

            # выставляем положение с другого конца (мир замкнут по кругу)
            if j >= map_width:
                j -= map_width
            if j < 0:
                j += map_width

            i = y + y_delta

            if i >= map_height:
                i -= map_height
            if i < 0:
                i += map_height

            # возможность прохода на клетку проверяется по старой карте
            new_position_cell = old_map[i][j]
            if not new_position_cell.is_solid:
                # если клетка может сделать шаг, то в старой карте она блокирует позициую куда собирается встать на
                # новой итерации, а свое перемещение она фиксирует на новой карте. заблокированная ячейка в
                # старой карте не даст двум клеткам встать в одно и тоже место и при этом не вызывает бага с тем
                # что ячейка воздуха становится непроницаемой
                new_position_cell.busy()
                new_map[y][x] = Empty().set_id(cell.get_id)
                new_map[i][j] = cell.set_id(new_position_cell.get_id)
            else:
                # если клетка заблокирована, куда нужно сделать шаг, то все равно нужно обновить объект, пусть он
                # и остался на месте
                new_map[y][x] = cell

        if move is None and self._next is not None:
            result = self._next.handle(cell, coordinates, old_map, new_map)

        return result


class EatHerbFood(Handler):
    pass
