from random import Random, randrange as default_randrange
from typing import Optional

from .._Binnable import Binnable
from .._typing import KeyType
from ._Binner import Binner


class RandomBinner(Binner[KeyType, int]):
    """
    Binner which bins items randomly into a set number of bins.
    """
    def __init__(self,
                 num_bins: int,
                 rand: Optional[Random] = None):
        self.__rand: Optional[Random] = rand
        self.__num_bins: int = num_bins

    def bin(self, item: Binnable[KeyType]) -> int:
        # Use the given random if available, or the default if not
        randrange = self.__rand.randrange if self.__rand is not None else default_randrange

        return randrange(self.__num_bins)