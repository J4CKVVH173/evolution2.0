import uuid
from abc import abstractmethod

import numpy as np
from action.move import Move, MoveBuilder
from cells.base import BaseCell
from neural.neural_network import NeuralNetwork
from settings import CELL_HERBIVORE


class BaseLive(BaseCell):
    """Базовый класс для живых клеток."""

    BORN_SUBSCRIBERS = []  # подписчики для события рождения новой клетки
    DEATH_SUBSCRIBERS = []  # подписчики для события смерти клетки

    def __init__(self, genome=None, health=40, clan=None, color=CELL_HERBIVORE):
        super().__init__()
        self.HEALTH = health
        self.FIXED = False
        self.HIDE_WEIGHTS = None
        self.OUT_WEIGHTS = None
        self.COLOR = color
        # переменная определяющая имя клана, чтобы можно было определить клетки с одинаковым геномом
        # дети, с мутировавшим геномом, относятся к другому клану
        if clan is None:
            self.CLAN_NAME = uuid.uuid4()
        else:
            self.CLAN_NAME = clan

        self._move_info = MoveBuilder()

        if genome:
            self._set_genome(*genome)
        else:
            self._generate_genome()

        self.neurons = NeuralNetwork(self.HIDE_WEIGHTS, self.OUT_WEIGHTS)

    @abstractmethod
    def got_food(self):
        """Метод для установки внутреннего состояния клетки, после того как клетка поела."""
        pass

    @abstractmethod
    def make_move(self):
        """Метод для совершения шага клеткой."""
        pass

    @classmethod
    def add_born_sub(cls, subscriber):
        """Метод для добавления подписчика на событие рождения клетки.

        Args:
            subscriber (callack): Колбэк, который будет вызываться при обработке события на которое подписался объект
        """
        cls.BORN_SUBSCRIBERS.append(subscriber)

    @classmethod
    def add_death_sub(cls, subscriber):
        """Метод для добавления подписчика на событие смерти клетки.

        Args:
            subscriber (callback): Колбэк, который будет вызываться при обработке события на которое подписался объект
        """
        cls.DEATH_SUBSCRIBERS.append(subscriber)

    def _set_genome(self, hide_weights: np.array, out_weights: np.array) -> None:
        """Метод производит установку весов, который отвечает за поведение клетки и представляет ее геном.

        Args:
            hide_weights (np.array): Веса для скрытого слоя
            out_weights (np.array): Веса для слова вывода информации.
        """
        self.HIDE_WEIGHTS = hide_weights
        self.OUT_WEIGHTS = out_weights

    def _generate_genome(self) -> None:
        """Метод для начальной генерации случайных весов для генома клетки."""
        self._set_genome(
            np.random.uniform(low=-5.0, high=5.0, size=(9, 16)), np.random.uniform(low=-5.0, high=5.0, size=(16, 9))
        )

    def save_genome(self) -> list:
        """Метод возвращает текущий геном клетки.

        Returns:
            list: Возвращает массив весов, которые представляет геном клетки.
                Веса расположены в порядке расположения слоев.
        """
        return [np.copy(self.HIDE_WEIGHTS), np.copy(self.OUT_WEIGHTS)]

    def get_move_info(self) -> Move:
        """Метод формирует объект класса Move с информацией о движении клеток и возвращает его.

        Returns:
            Move: Объект класса Move.
        """
        return self._move_info.build()

    def reset_move_info(self) -> None:
        """Метод производит сброс настроек об информации движения клетки."""
        self._move_info.reset()

    def _change_health(self, count: int = -1):
        """Метод для изменения здоровья клетки.

        Вызывается в начале каждого движения клетки

        Args:
            count (int, optional): Значение на которое здоровье клетки должно быть уменьшено. Defaults to -1.
        """
        # меняем здоровье клетки
        self.HEALTH += count
        # проверяем сразу, если клетка умерла после изменения здоровья, вызываем всех подписчиков подписанных
        # на данное событие
        if self.is_dead:
            for sub in self.DEATH_SUBSCRIBERS:
                sub.die_cell(self)

    def reprodaction(self) -> "BaseLive":
        """Интерфейс прототипа для создания копии клетки.

        Returns:
            BaseLive: Будет возвращена копия клетки.
        """
        pass

    def set_color(self, color: str) -> None:
        """Метод для установки цвета текущей ячейки.

        Args:
            color (str): Цвет устанавливаемый для ячейки
        """
        self.COLOR = color

    @property
    def get_color(self) -> str:
        return self.COLOR

    @property
    def get_clan_name(self) -> str:
        return self.CLAN_NAME

    @staticmethod
    @property
    def can_reproduction(self):
        """Свойство определяет, может ли клетка размножаться или нет."""
        pass

    @property
    def is_dead(self) -> bool:
        """Свойство возвращает информацию о том, жива ли клетка.

        Если здоровье клетки 0 или меньше, то она считается мертвой.
        Returns:
            bool: True - если мертва, False - если жива
        """
        return self.HEALTH <= 0

    @property
    def get_health(self) -> int:
        """Свойство возвращающее текущее здоровье клетки.

        Returns:
            int: здоровье клетки
        """
        return self.HEALTH
