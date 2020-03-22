from typing import Iterable, TypeVar, List

# The type of element in the iterable
ElementType = TypeVar("ElementType")


def conservatively_cache(items: Iterable[ElementType]) -> List[ElementType]:
    """
    Caches the iterable in a list, unless it already is a list.

    :param items:   The iterable of items.
    :return:        The list of items.
    """
    return items if isinstance(items, list) else list(items)
