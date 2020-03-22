from math import ceil
from numbers import Real
from typing import Optional, Tuple, List

from ._TwoPassBinner import TwoPassBinner
from .._Binnable import Binnable


class EqualWidthBinner(TwoPassBinner[Real, int]):
    """
    Binner which creates bins of equal size. Can be created by specifying the
    number of bins or the width of a bin.
    """
    def __init__(self, *, num_bins: Optional[int] = None, bin_width: Optional[Real] = None):
        # Can only specify one of bin_width and num_bins
        if (bin_width is None) == (num_bins is None):
            raise ValueError("Must specify exactly one of bin_width and num_bins")

        # Make sure at least one bin is specified if at all
        if num_bins is not None and num_bins < 1:
            raise ValueError(f"Number of bins must be positive, got {num_bins}")

        # Make sure the bin width if positive if specified at all
        if bin_width is not None and bin_width <= 0.0:
            raise ValueError(f"Bin width must be positive, got {bin_width}")

        self._min: Real = 0
        self._max: Real = 0

        self._num_bins: Optional[int] = num_bins
        self._bin_width: Optional[Real] = bin_width

    def _find_min_max(self, items: List[Binnable[Real]]) -> Tuple[Real, Real]:
        """
        Finds the minimum and maximum bin key value for the given items.

        :param items:   The binnable items.
        :return:        The min and max bin-key.
        """
        return (
            min(Binnable.map_bin_keys(items), default=0),
            max(Binnable.map_bin_keys(items), default=0)
        )

    def _configure(self, items: List[Binnable[Real]]):
        # Find the min/max keys
        self._min, self._max = self._find_min_max(items)

        # Calculate the value that wasn't supplied explicitly
        if self._bin_width is None:
            self._bin_width = (self._max - self._min) / self._num_bins
        else:
            self._num_bins = ceil((self._max - self._min) / self._bin_width)

    def _bin(self, key: Real) -> int:
        # Hack to make sure items with bin_key == self._max go in the last bin
        if key == self._max:
            return self._num_bins - 1

        # Calculate the bin that the key should go into
        return (key - self._min) // self._bin_width
