from cells import BaseCell


def duck_typing_lists_equals(l1: list, l2: list) -> bool:
    """Функция для сравнения списка двух объктов через метод утиной типизации объекта.

    Args:
        l1 (list): Первый список для сравнения
        l2 (list): Второй список для сравнения

    Returns:
        bool: Возвращает булевское значние True если списки равны и False если не равны.
    """
    if not len(l1) == len(l2):
        return False

    for i, el in enumerate(l1):
        if not el.duck_typing() == l2[i].duck_typing():
            return False
    return True


def duck_typing_elements_equals(el1: BaseCell, el2: BaseCell) -> bool:
    """Функция для сравнения двух объектов через метод утиной типизации объекта.

    Args:
        el1 (BaseCell): Первый объект для сравнения
        el2 (BaseCell): Второй объект для сравнения

    Returns:
        bool: Возвращает булевское значние True если объекты равны и False если не равны.
    """
    if not el1.duck_typing() == el2.duck_typing():
        return False
    return True
