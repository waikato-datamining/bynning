from abc import abstractmethod
from typing import Generic, Iterator, Iterable

from ._typing import KeyType, ItemType


class BinKeyExtractor(Generic[ItemType, KeyType]):
    """
    Interface for classes which extract bin-keys from items.
    """
    @abstractmethod
    def extract_bin_key(self, item: ItemType) -> KeyType:
        """
        Extracts a bin-key from a given object.

        :param item:     The object to extract a bin-key from.
        :return:        The bin-key.
        """
        pass

    def extract_all(self, items: Iterable[ItemType]) -> Iterator[KeyType]:
        """
        Extracts bin-keys for all the given items.

        :param items:   The items to extract bin-keys for.
        :return:        An iterator of bin-keys.
        """
        return map(self.extract_bin_key, items)
