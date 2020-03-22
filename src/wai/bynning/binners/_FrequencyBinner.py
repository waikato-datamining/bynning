from numbers import Real
from typing import List

from ..util import frequency_divide
from .._Binnable import Binnable
from .._typing import ItemType
from ._TwoPassBinner import TwoPassBinner


class FrequencyBinner(TwoPassBinner[Real, int]):
    """
    Puts items into bins such that all bins have the same number
    of items in them, up to a possible difference of 1. Items are
    ordered by the values of their bin-keys (which are real values).
    """
    def __init__(self, num_bins: int):
        if num_bins < 1:
            raise ValueError("Must specify at least one bin")

        self._num_bins: int = num_bins
        self._ranges: List[range] = []
        self._range_index: int = 0
        self._index: int = 0

    def _configure(self, items: List[ItemType]):
        # Sort the items by key
        items.sort(key=Binnable.map_bin_key)

        # Create ranges of items for each bin
        self._ranges = [frequency_divide(len(items), self._num_bins, bin) for bin in range(self._num_bins)]

    def _reset(self):
        self._range_index = 0
        self._index = 0

    def _bin(self, key: Real) -> int:
        # The bin is the range we are in
        label = self._range_index

        # Move to the next item
        self._index += 1

        # If we've completed this range, move to the next range
        if self._index not in self._ranges[self._range_index]:
            self._range_index += 1

        return label
