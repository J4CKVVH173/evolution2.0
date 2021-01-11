from abc import ABC, abstractmethod

from typing import Tuple

from cells import Empty, BaseCell, PlantFood


class Handler(ABC):
    """Абстрактный класс для цепочки обработчиков для арбитера."""

    _next: "Handler" = None

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance

    @abstractmethod
    def handle(
        self,
        cell: BaseCell,
        coordinates: Tuple[int, int],
        old_map: Tuple[Tuple[BaseCell]],
        new_map: Tuple[Tuple[BaseCell]],
    ) -> bool:
        """Метод для обработки вызова цепочки звена.

        Args:
            cell (BaseCell): ячейка которая совершает движение
            coordinates (Tuple[int, int]): координаты положения ячейки на карте
            old_map (Tuple[Tuple[BaseCell]]): старое представление карты
            new_map (Tuple[Tuple[BaseCell]]): новое представление карты

        Returns:
            bool: True - если хоть какое то звено цепи обработало вызов, False если никто не обработал вызов.
        """
        pass

    def set_next(self, next_link: "Handler") -> "Handler":
        """Метод для установки следующей цепочки звена.

        Returns:
            next_link (Handler): Следующее звено цепочки вызовов.
        """
        self._next = next_link
        return self

    @staticmethod
    def _action_coordinates(
        coordinates: Tuple[int, int], move_delta: Tuple[int, int], map_size: Tuple[int, int]
    ) -> Tuple[int, int]:
        """Метод производит расчет координат ячейки, с которыми клетка должна произвести взаимодействие.

        Args:
            coordinates (Tuple[int, int]): Текущее положение клетки (x, y)
            move_delta (Tuple[int, int]): Дельта смещения (d_x, d_y)
            map_size (Tuple[int, int]): Размеры карты (ширина, высотка)

        Returns:
            Tuple[int, int]: Ячейка с которой клетка должно совершить взаимодействие (переместиться или
             съесть или тп)
        """
        x, y = coordinates
        x_delta, y_delta = move_delta
        map_width, map_height = map_size

        i = x + x_delta  # высчитывается новая координата положения
        j = y + y_delta

        # выставляем положение с другого конца (мир замкнут по кругу)
        if i >= map_width:
            i -= map_width
        if i < 0:
            i += map_width

        if j >= map_height:
            j -= map_height
        if j < 0:
            j += map_height

        return i, j


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
    """Звено обрабатывающее движение клетки."""

    def handle(
        self,
        cell: BaseCell,
        coordinates: Tuple[int, int],
        old_map: Tuple[Tuple[BaseCell]],
        new_map: Tuple[Tuple[BaseCell]],
    ):
        move = cell.get_move_info().get_move()
        result = False

        if move is not None:
            x, y = coordinates
            map_width = len(old_map[0])
            map_height = len(old_map)

            i, j = self._action_coordinates([x, y], move, [map_width, map_height])

            # возможность прохода на клетку проверяется по старой карте
            new_position_cell = old_map[j][i]
            if not new_position_cell.is_solid:
                # если клетка может сделать шаг, то в старой карте она блокирует позициую куда собирается встать на
                # новой итерации, а свое перемещение она фиксирует на новой карте. заблокированная ячейка в
                # старой карте не даст двум клеткам встать в одно и тоже место и при этом не вызывает бага с тем
                # что ячейка воздуха становится непроницаемой
                new_position_cell.busy()
                new_map[y][x] = Empty().set_id(cell.get_id)
                new_map[j][i] = cell.set_id(new_position_cell.get_id)
            else:
                # если клетка заблокирована, куда нужно сделать шаг, то все равно нужно обновить состояние объекта
                # на новой карте объект, пусть он и остался на месте
                new_map[y][x] = cell
            return True

        if move is None and self._next is not None:
            result = self._next.handle(cell, coordinates, old_map, new_map)

        return result


class EatHerbFood(Handler):
    """Звено обрабатывающее укус травоядной клетки."""

    def handle(
        self,
        cell: BaseCell,
        coordinates: Tuple[int, int],
        old_map: Tuple[Tuple[BaseCell]],
        new_map: Tuple[Tuple[BaseCell]],
    ):
        bite = cell.get_move_info().get_bite()
        result = False

        if bite is not None:
            x, y = coordinates
            map_width = len(old_map[0])
            map_height = len(old_map)

            i, j = self._action_coordinates([x, y], bite, [map_width, map_height])

            target_cell = old_map[j][i]
            if isinstance(target_cell, PlantFood) and target_cell.can_eat:
                target_cell.eat()
                cell.got_food()
                new_map[j][i] = Empty().set_id(target_cell.get_id)
            new_map[y][x] = cell
            return True

        if bite is None and self._next is not None:
            result = self._next.handle(cell, coordinates, old_map, new_map)

        return result


class Reproduction(Handler):
    """Звено для размножения клеток."""

    def handle(
        self,
        cell: BaseCell,
        coordinates: Tuple[int, int],
        old_map: Tuple[Tuple[BaseCell]],
        new_map: Tuple[Tuple[BaseCell]],
    ):
        is_reproduction = cell.get_move_info().is_reproduction()
        result = False

        if is_reproduction and cell.can_reproduction:
            x, y = coordinates
            map_width = len(old_map[0])
            map_height = len(old_map)

            cell_clone_position = old_map[y][x]

            x_delta = y_delta = -1

            # если клетка может размножаться, проверяем есть ле место, где может расположиться копия
            while cell_clone_position.is_solid:
                i, j = self._action_coordinates([x, y], [x_delta, y_delta], [map_width, map_height])
                cell_clone_position = old_map[j][i]

                if y_delta < 1:
                    y_delta += 1

                if y_delta == 1:
                    x_delta += 1

                if x_delta == 2:
                    # если x_delta > 1 и y_delta == 1, получается свободного места рядом с клеткой нет, но обработать
                    # данное звено смогло, значит просто завершаем обработку
                    x, y = coordinates
                    new_map[y][x] = cell
                    return True

            # если есть место где располагать новую клетку, начинается процесс репродукции
            cell_clone = cell.reprodaction()
            cell_clone.set_id(cell_clone_position.get_id)
            cell_clone_position.busy()
            new_map[y][x] = cell
            new_map[j][i] = cell_clone
            return True

        if self._next is not None:
            result = self._next.handle(cell, coordinates, old_map, new_map)

        return result
