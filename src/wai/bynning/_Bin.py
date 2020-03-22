from typing import Generic, Iterator, List

from ._Binnable import Binnable
from ._typing import LabelType, KeyType, ItemType


class Bin(Binnable[LabelType], Generic[LabelType, ItemType]):
    """
    Class representing a single bin of binnable items.
    """
    def __init__(self, label: LabelType):
        self._label: LabelType = label
        self._items: List[ItemType] = []

    def add_item(self, item: ItemType):
        """
        Adds a single item to the bin.

        :param item:    The item.
        """
        self._items.append(item)

    @property
    def bin_key(self) -> LabelType:
        """
        Gets the bin-key for binning this bin, which is
        the label.
        """
        return self.label

    @property
    def label(self) -> LabelType:
        """
        Gets the label for this bin.
        """
        return self._label

    def __contains__(self, item: ItemType) -> bool:
        """
        Checks if a given item is in this bin.

        :param item:    The item.
        :return:        True if the item is in this bin,
                        False if not.
        """
        return item in self._items

    def contains_key(self, key: KeyType) -> bool:
        """
        Checks if any item in the bin has the given bin-key.

        :param key:     The bin-key.
        :return:        True if an item in the bin has the given bin-key,
                        False if not.
        """
        return any(item.bin_key == key for item in self._items)

    def __iter__(self) -> Iterator[ItemType]:
        """
        Returns an iterator over the items in this bin.
        """
        return iter(self._items)

    def __getitem__(self, index: int) -> ItemType:
        """
        Gets an item from this bin by index.

        :param index:   The positional index of the item to get.
        :return:        The item.
        """
        return self._items[index]

    def get_items_by_key(self, key: KeyType) -> Iterator[ItemType]:
        """
        Gets the items in this bin that have the given bin-key.

        :param key:     The key to search for.
        :return:        The items.
        """
        return (item for item in self._items if item.bin_key == key)

    def __len__(self) -> int:
        """
        Gets the number of items in this bin.
        """
        return len(self._items)

    def __str__(self) -> str:
        indented_items: str = ',\n  '.join(map(str, self))
        return f"{self._label}:\n  {indented_items}"
