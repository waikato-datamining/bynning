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
