from itertools import chain
from typing import Generic, List, Union, Iterator, Iterable, Optional

from ._BinItem import BinItem
from ._Binnable import Binnable
from ._typing import LabelType, KeyType, ItemType


class Bin(Binnable[LabelType], Generic[ItemType, LabelType]):
    """
    Class representing a single bin of binnable items.
    """
    def __init__(self, label: LabelType, items: Optional[Iterable[ItemType]] = None):
        self.__label: LabelType = label
        self.__items: List[ItemType] = list(items) if items is not None else []

    def get_bin_key(self) -> LabelType:
        """
        Gets the bin-key for binning this bin, which is
        the label.
        """
        return self.label()

    def label(self) -> LabelType:
        """
        Gets the label for this bin.
        """
        return self.__label

    def add(self, item: ItemType):
        """
        Adds a single binnable item to this bin.

        :param item:    The item to add.
        """
        self.__items.append(item)

    def add_all(self, items: Iterable[ItemType]):
        """
        Adds a series of binnable items to this bin.

        :param items:   The items to add.
        """
        for item in items:
            self.__items.append(item)

    def merge(self, other: 'Bin[ItemType, LabelType]'):
        """
        Adds all the items from another bin to this one.

        :param other:   The bin to merge the items from.
        """
        self.add_all(other)

    def sort(self, reverse: bool = False):
        """
        Sorts the items in this bin in place.

        :param reverse:     Set to True to sort in descending order.
        """
        self.__items.sort(key=Binnable.get_bin_key_static, reverse=reverse)

    def delayer(self) -> bool:
        """
        Removes one layer of wrapping from this bin.

        :return:    Whether delayering was possible.
        """
        if self.items_are_bins():
            self.__items = list(chain(*self))
        elif self.items_are_wrapped():
            self.__items = list(map(BinItem.payload, self))
        else:
            return False

        return True

    def __contains__(self, item: Union[ItemType, KeyType]) -> bool:
        """
        Checks if a given item is in this bin.

        :param item:    The item, or a bin-key.
        :return:        True if the item (or an item with the given key) is in
                        this bin, False if not.
        """
        if isinstance(item, Binnable):
            return item in self.__items
        else:
            return item in map(Binnable.get_bin_key_static, self.__items)

    def __iter__(self) -> Iterator[ItemType]:
        """
        Returns an iterator over the items in this bin.
        """
        return iter(self.__items)

    def __getitem__(self, index: int) -> ItemType:
        """
        Gets an item from this bin by index.

        :param index:   The positional index of the item to get.
        :return:        The item.
        """
        return self.__items[index]

    def get_items_by_key(self, key: KeyType) -> List[ItemType]:
        """
        Gets the list of items in this bin that have
        the given bin-key.

        :param key:     The key to search for.
        :return:        The list of items.
        """
        return [item for item in self if item.get_bin_key() == key]

    def __len__(self) -> int:
        """
        Gets the number of items in this bin.
        """
        return len(self.__items)

    def items_are_bins(self) -> bool:
        """
        Whether the items in this bin are themselves bins.
        """
        return len(self) > 0 and isinstance(self.__items[0], Bin)

    def items_are_wrapped(self) -> bool:
        """
        Whether the items in this bin are wrapped by the BinItem class.
        """
        if len(self) > 0:
            first = self.__items[0]
            if isinstance(first, BinItem):
                return first.payload_is_binnable()

        return False

    def __str__(self) -> str:
        return f"{self.__label}: {', '.join(map(str, self))}"
