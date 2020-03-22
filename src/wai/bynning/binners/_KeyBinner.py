from .._typing import KeyType
from ._Binner import Binner


class KeyBinner(Binner[KeyType, KeyType]):
    """
    Binner which just makes a new bin per encountered bin-key.
    """
    def _bin(self, key: KeyType) -> KeyType:
        return key
