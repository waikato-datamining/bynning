from math import ceil, sqrt
from numbers import Real
from typing import Tuple

from .._Binnable import Binnable
from ._EqualWidthBinner import EqualWidthBinner


class SquareRootChoiceBinner(EqualWidthBinner):
    """
    Equal-width binner that uses the square-root of the
    number of binned items as the number of bins.
    """
    def __init__(self):
        # Doesn't matter how many bins we set here as it is overridden
        # in _configure
        super().__init__(num_bins=1)

    def _configure(self, items: Tuple[Binnable[Real], ...]):
        self._num_bins = int(ceil(sqrt(len(items))))

        super()._configure(items)
