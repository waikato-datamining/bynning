from math import ceil
from numbers import Real
from typing import List

from .._Binnable import Binnable
from ._EqualWidthBinner import EqualWidthBinner


class RiceRuleBinner(EqualWidthBinner):
    """
    Equal-width binner that uses Sturges' formula to
    determine the number of bins.
    """
    def __init__(self):
        # Doesn't matter how many bins we set here as it is overridden
        # in _configure
        super().__init__(num_bins=1)

    def _configure(self, items: List[Binnable[Real]]):
        self._num_bins = int(ceil(2 * len(items) ** (1/3)))

        super()._configure(items)
