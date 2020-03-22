from abc import abstractmethod
from typing import Generic, Iterator, Iterable, Tuple

from .._Bin import Bin
from .._Binning import Binning
from .._typing import KeyType, LabelType, ItemType


class Binner(Generic[KeyType, LabelType]):
    """
    Interface for classes which sort binnable items into bins via their
    bin-keys.
    """
    def _reset(self):
        """
        Resets the binner between binnings.
        """
        pass

    @abstractmethod
    def _bin(self, key: KeyType) -> LabelType:
        """
        Returns the bin label of the bin that items with the given
        bin-key should go into.

        :param key:     The bin-key to bin.
        :return:        The bin label.
        """
        pass

    def _bin_item(self, item: ItemType) -> LabelType:
        """
        Returns the bin label of the bin that the given item
        should go into.

        :param item:    The item to bin.
        :return:        The bin label.
        """
        return self._bin(item.bin_key)

    def _bin_items(self, items: Iterable[ItemType]) -> Iterator[Tuple[LabelType, ItemType]]:
        """
        Returns the bin labels for all the given items.

        :param items:   The items to bin.
        :return:        An iterator over the items and their respective bin-labels.
        """
        # Reset the binner
        self._reset()

        return ((self._bin_item(item), item) for item in items)

    def bin(self, items: Iterable[ItemType]) -> Binning[ItemType, LabelType]:
        """
        Creates a binning of the given items.

        :param items:   The items.
        :return:        The binning.
        """
        bins = {}
        for label, item in self._bin_items(items):
            if label not in bins:
                bins[label] = Bin(label)
            bins[label].add_item(item)

        return Binning(bins.values())
