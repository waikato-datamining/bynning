from .._Binnable import Binnable
from .._typing import KeyType
from ._Binner import Binner


class StratifyingBinner(Binner[KeyType, int]):
    """
    Binner which cyclically stratifies items over a number of bins.
    """
    def __init__(self, num_folds: int):
        self._num_folds: int = num_folds
        self._next: int = 0

    def bin(self, item: Binnable[KeyType]) -> int:
        # Get the next stratification label to use
        label: int = self._next

        # Increment the next label
        self._next += 1
        self._next %= self._num_folds

        return label
