from collections import OrderedDict
from itertools import chain
from typing import Generic, Iterator, Union, Iterable

from ._Bin import Bin
from ._typing import KeyType, ItemType, LabelType


class Binning(Generic[ItemType, LabelType]):
    """
    Class representing a binning of a set of items into bins.
    """
    def __init__(self, bins: Iterable[Bin[LabelType, ItemType]]):
        self._bins: OrderedDict[LabelType, Bin[LabelType, ItemType]] = OrderedDict(
            (bin.label, bin) for bin in bins
        )

    def __contains__(self, label: LabelType) -> bool:
        """
        Whether a bin with the given label is in this binning.

        :param label:   The bin label.
        :return:        True if the bin is in this binning,
                        False if not.
        """
        return label in self._bins.keys()

    def contains_item(self, item: Union[ItemType, KeyType]) -> bool:
        """
        Whether the given item is in any of the bins in this binning.

        :param item:    The item, or its bin-key.
        :return:        True if the item is in this binning,
                        False if not.
        """
        for bin in self._bins.values():
            if item in bin:
                return True

        return False

    def contains_key(self, key: KeyType) -> bool:
        """
        Whether an item with the given key is in this binning.

        :param key:     The bin key to look for.
        :return:        True if an item with the bin-key is in this binning,
                        False if not.
        """
        for bin in self._bins.values():
            if bin.contains_key(key):
                return True

        return False

    def __iter__(self) -> Iterator[Bin[LabelType, ItemType]]:
        """
        Returns an iterator over the bins in this binning.
        """
        return iter(self._bins.values())

    def item_iterator(self) -> Iterator[ItemType]:
        """
        Returns an iterator over the items in the bins in this binning.
        """
        return chain(*self)

    def __getitem__(self, item: LabelType) -> Bin[LabelType, ItemType]:
        """
        Gets the bin with the given label.

        :param item:    The bin label.
        :return:        The bin.
        """
        return self._bins[item]

    def get_item(self, index: int) -> ItemType:
        """
        Gets the indexed item from amongst all the items in the bins.

        :param index:   The index of the item to get.
        :return:        The binnable item.
        """
        # Wrap the index
        index = range(self.num_items())[index]

        # Find the item
        for bin in self:
            if index < len(bin):
                return bin[index]
            else:
                index -= len(bin)

    def __len__(self) -> int:
        """
        Gets the number of bins in this binning.
        """
        return len(self._bins)

    def num_items(self) -> int:
        """
        Gets the total number of items across all bins.
        """
        return sum(map(len, self))

    def __str__(self):
        return '\n'.join(map(str, self))
