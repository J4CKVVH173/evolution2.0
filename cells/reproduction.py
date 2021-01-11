import random

from numpy import array

from cells.live.base import BaseLive


class Reprodaction:
    """Класс отвечающий за размножение клеток."""

    def crossing(self, cell_one: BaseLive, cell_two: BaseLive) -> array:
        """Метод производит скрещивание двух переданных клеток и возвращает скрещенный геном.

        Args:
            cell_one (BaseLive): Первая клетка для скрещивания
            cell_two (BaseLive): Вторая клетка для скрещивания

        Returns:
            list: геном скрещенной клетки.
        """
        first_genome = cell_one.save_genome()
        second_genome = cell_two.save_genome()

        counter = 0

        new_genome = list()
        for i, layer in enumerate(first_genome):
            new_layer = list()
            for j, gen in enumerate(layer):
                new_gen = list()
                for k, nucleotide in enumerate(gen):
                    counter += 1
                    if counter % 2:
                        new_gen.append(nucleotide)  # noqa
                    else:
                        new_gen.append(second_genome[i][j][k])
                new_layer.append(new_gen.copy())
            new_genome.append(new_layer.copy())

        return array(new_genome)

    def mutation(self, genome: array) -> array:
        """Метод производит мутацию переданного в него генома.

        Args:
            genome (array): Геном который должен быть подвержен мутации

        Returns:
            array: Мутировавший геном.
        """

        new_genome = list()
        for gen in genome:
            new_gen = list()
            for nucleotide in gen:
                if random.random() < 0.1:
                    new_gen.append(nucleotide + random.choice([-1, 1]) * 0.15)
                else:
                    new_gen.append(nucleotide)
            new_genome.append(new_gen.copy())

        return array(new_genome)
