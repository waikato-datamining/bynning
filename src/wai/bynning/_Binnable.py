from abc import abstractmethod
from typing import Generic

from ._typing import KeyType


class Binnable(Generic[KeyType]):
    """
    Interface for objects that can be sorted into bins.
    """
    @abstractmethod
    def get_bin_key(self) -> KeyType:
        """
        Gets the bin key to use to sort this binnable into
        a bin.
        """
        pass

    @staticmethod
    def get_bin_key_static(binnable: 'Binnable[KeyType]') -> KeyType:
        """
        Static accessor of the binnable's get_bin_key method (for
        sorting routines).

        :param binnable:    The binnable to get the bin key from.
        :return:            The bin key.
        """
        return binnable.get_bin_key()
