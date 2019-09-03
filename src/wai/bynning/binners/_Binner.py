from abc import abstractmethod
from typing import Generic, Iterator, Iterable, Tuple

from .._Binnable import Binnable
from .._typing import KeyType, LabelType


class Binner(Generic[KeyType, LabelType]):
    """
    Interface for classes which sort binnable items into bins via their
    bin-keys.
    """
    @abstractmethod
    def bin(self, item: Binnable[KeyType]) -> LabelType:
        """
        Returns the bin label of the bin that the given
        binnable item should go into.

        :param item:    The item to bin.
        :return:        The bin label.
        """
        pass

    def bin_all(self, items: Iterable[Binnable[KeyType]]) -> Iterator[Tuple[Binnable[KeyType], LabelType]]:
        """
        Returns the bin labels for all the given items.

        :param items:   The items to bin.
        :return:        An iterator over the items and their respective bin-labels.
        """
        return ((item, self.bin(item)) for item in items)
