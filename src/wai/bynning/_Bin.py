from typing import Generic, List, Union, Iterator, Iterable, Optional

from ._Binnable import Binnable
from ._typing import LabelType, KeyType


class Bin(Binnable[LabelType], Generic[LabelType, KeyType]):
    """
    Class representing a single bin of binnable items.
    """
    def __init__(self, label: LabelType, items: Optional[Iterable[Binnable[KeyType]]] = None):
        self.__label: LabelType = label
        self.__items: List[Binnable[KeyType]] = list(items) if items is not None else []

    def get_bin_key(self) -> LabelType:
        return self.label()

    def label(self) -> LabelType:
        """
        Gets the label for this bin.
        """
        return self.__label

    def add(self, item: Binnable[KeyType]):
        """
        Adds a single binnable item to this bin.

        :param item:    The item to add.
        """
        self.__items.append(item)

    def add_all(self, items: Iterable[Binnable[KeyType]]):
        """
        Adds a series of binnable items to this bin.

        :param items:   The items to add.
        """
        for item in items:
            self.__items.append(item)

    def merge(self, other: 'Bin[LabelType, KeyType]'):
        """
        Adds all the items from another bin to this one.

        :param other:   The bin to merge the items from.
        """
        self.add(*iter(other))

    def sort(self, reverse: bool = False):
        """
        Sorts the items in this bin in place.

        :param reverse:     Set to True to sort in descending order.
        """
        self.__items.sort(key=Binnable.get_bin_key, reverse=reverse)

    def __contains__(self, item: Union[Binnable[KeyType], KeyType]) -> bool:
        if isinstance(item, Binnable):
            return item in self.__items
        else:
            return item in map(Binnable.get_bin_key, self.__items)

    def __iter__(self) -> Iterator[Binnable[KeyType]]:
        return iter(self.__items)

    def __getitem__(self, index: int) -> Binnable[KeyType]:
        return self.__items[index]

    def get_items_by_key(self, key: KeyType) -> List[Binnable[KeyType]]:
        """
        Gets the list of items in this bin that have
        the given bin-key.

        :param key:     The key to search for.
        :return:        The list of items.
        """
        return [item for item in self if item.get_bin_key() == key]

    def __len__(self) -> int:
        return len(self.__items)
