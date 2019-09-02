from .._Binnable import Binnable
from .._typing import KeyType
from ._Binner import Binner


class KeyBinner(Binner[KeyType, KeyType]):
    """
    Binner which just makes a new bin per encountered bin-key.
    """
    def bin(self, item: Binnable[KeyType]) -> KeyType:
        return item.get_bin_key()
