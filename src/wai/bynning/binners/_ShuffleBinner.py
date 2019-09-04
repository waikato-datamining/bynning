from random import Random, shuffle as default_shuffle
from typing import Tuple, Optional, List

from .._Binnable import Binnable
from .._typing import KeyType
from ._ConfiguredBinner import ConfiguredBinner


class ShuffleBinner(ConfiguredBinner[KeyType, int]):
    """
    Binner which creates a random ordering of the items by putting
    them each in their own bin.
    """
    def __init__(self, rand: Optional[Random] = None):
        super().__init__()

        self._rand: Optional[Random] = rand

        self.__ordering: List[int] = []
        self.__last_index: int = -1

    def _configure(self, items: Tuple[Binnable[KeyType], ...]):
        # Use the given RNG's shuffle if available, or the default if not
        shuffle = self._rand.shuffle if self._rand is not None else default_shuffle

        # Create an ordered list of indices
        self.__ordering = list(range(len(items)))

        # Shuffle it
        shuffle(self.__ordering)

    def bin(self, item: Binnable[KeyType]) -> int:
        # Move to the next index
        self.__last_index += 1

        # Return the permutation index for this item
        return self.__ordering[self.__last_index]
