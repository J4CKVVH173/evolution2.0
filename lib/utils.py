def duck_typing_lists_equals(l1, l2) -> bool:
    if not len(l1) == len(l2):
        return False

    for i, el in enumerate(l1):
        if not el.duck_typing() == l2[i].duck_typing():
            return False
    return True


def duck_typing_elements_equals(el1, el2) -> bool:
    if not el1.duck_typing() == el2.duck_typing():
        return False
    return True
