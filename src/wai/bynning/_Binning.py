from collections import OrderedDict
from itertools import chain
from typing import Generic, Iterator, Union, Iterable, Optional, overload, TypeVar

from ._Bin import Bin
from .binners import Binner
from ._typing import KeyType, ItemType, LabelType

NewLabelType = TypeVar("NewLabelType")  # Type of label after rebinning


class Binning(Generic[ItemType, LabelType]):
    """
    Class representing a binning of a set of items into bins.
    """
    def __init__(self, binner: Binner[KeyType, LabelType], items: Optional[Iterable[ItemType]] = None):
        self._binner: Binner[KeyType, LabelType] = binner
        self._bins: OrderedDict[LabelType, Bin[ItemType, LabelType]] = OrderedDict()

        # Bin any initial items
        if items is not None:
            self.bin(items)

    def binner(self) -> Binner[KeyType, LabelType]:
        """
        Gets the binner used for this binning.
        """
        return self._binner

    def bin(self, items: Iterable[ItemType]):
        """
        Adds the given items to the bins in this binning.

        :param items:   The items to add.
        """
        for item, label in self._binner.bin_all(items):
            # Create a new bin if we have a new label
            if label not in self._bins:
                self._bins[label] = Bin[ItemType, LabelType](label)

            # Add the item to the correct bin
            self._bins[label].add(item)

    @overload
    def rebin(self,
              binner: Binner[KeyType, NewLabelType],
              against_bins: bool) -> 'Binning[ItemType, NewLabelType]':
        pass

    @overload
    def rebin(self,
              binner: Binner[LabelType, NewLabelType],
              against_bins: bool) -> 'Binning[Bin[ItemType, LabelType], NewLabelType]':
        pass

    def rebin(self,
              binner,
              against_bins=False):
        """
        Rebins the items in this binning using a new binner.

        :param binner:          The binner to use.
        :param against_bins:    Whether the given binner should be applied to the bins themselves
                                (grouped binning). Defaults to False (against items).
        :return:                The new binning.
        """
        return Binning(binner, self if against_bins else self.item_iterator())

    def __contains__(self, item: Union[Bin[ItemType, LabelType], LabelType]) -> bool:
        """
        Whether the given bin is in this binning.

        :param item:    The bin itself, or its label.
        :return:        True if the bin is in this binning,
                        False if not.
        """
        if isinstance(bin, Bin):
            return item in self._bins.values()
        else:
            return item in self._bins.keys()

    def contains_item(self, item: Union[ItemType, KeyType]) -> bool:
        """
        Whether the given item is in any of the bins in this binning.

        :param item:    The item, or its bin-key.
        :return:        True if the item is in this binning,
                        False if not.
        """
        return any(item in bin for bin in self)

    def __iter__(self) -> Iterator[Bin[ItemType, LabelType]]:
        """
        Returns an iterator over the bins in this binning.
        """
        return iter(self._bins.values())

    def item_iterator(self) -> Iterator[ItemType]:
        """
        Returns an iterator over the items in the bins in this binning.
        """
        return chain(*self)

    def ungrouping_iterator(self) -> Iterator:
        """
        Returns an iterator over the most-deeply-nested items in this binning
        (for grouped binning where bins may contain bins).
        """
        return chain(*(bin.ungrouping_iterator() for bin in self))

    def __getitem__(self, item: LabelType) -> Bin[ItemType, LabelType]:
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
        # Check index is in range
        max_index: int = self.total_num_items() - 1
        if not (0 <= index <= max_index):
            raise IndexError(f"Item index out of range ({index} not in [0:{max_index}])")

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

    def total_num_items(self) -> int:
        """
        Gets the total number of items across all bins.
        """
        return sum(map(len, self))

    def sort(self, reverse: bool = False):
        """
        Sorts the bins in this binning by label.

        :param reverse:     Whether to sort in reverse order.
        """
        # Create a list of the bins
        bin_list = list(self)

        # Sort the list by bin label
        bin_list.sort(key=Bin.label, reverse=reverse)

        # Clear the bins lookup of its current order
        self._bins.clear()

        # Add the bins in the sorted order
        for bin in bin_list:
            self._bins[bin.label()] = bin

    def sort_items(self, reverse: bool = False):
        """
        Sorts sorts the items in each bin in this binning.
        Does not change the bin order.

        :param reverse:     Whether to sort in reverse order.
        """
        for bin in self:
            bin.sort(reverse)
