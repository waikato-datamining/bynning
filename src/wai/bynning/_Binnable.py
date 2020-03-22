from abc import abstractmethod
from typing import Generic, Iterable, Iterator

from ._typing import KeyType


class Binnable(Generic[KeyType]):
    """
    Interface for objects that can be sorted into bins.
    """
    @property
    @abstractmethod
    def bin_key(self) -> KeyType:
        """
        Gets the bin key to use to sort this binnable into
        a bin.
        """
        pass

    @staticmethod
    def map_bin_key(binnable: 'Binnable[KeyType]') -> KeyType:
        """
        Maps a binnable to its bin key.

        :param binnable:    The binnable.
        :return:            Its bin-key.
        """
        return binnable.bin_key

    @staticmethod
    def map_bin_keys(binnables: Iterable['Binnable[KeyType]']) -> Iterator[KeyType]:
        """
        Maps a series of binnables to their bin-keys.

        :param binnables:   The binnables.
        :return:            An iterator over their bin-keys.
        """
        return (binnable.bin_key for binnable in binnables)
