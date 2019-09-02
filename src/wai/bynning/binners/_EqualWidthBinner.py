from math import ceil
from numbers import Real
from typing import Optional, Tuple

from ._ConfiguredBinner import ConfiguredBinner
from .._Binnable import Binnable


class EqualWidthBinner(ConfiguredBinner[Real, int]):
    """
    Binner which creates bins of equal size. Can be created by specifying the
    number of bins or the width of a bin.
    """
    def __init__(self, *, num_bins: Optional[int] = None, bin_width: Optional[Real] = None):
        super().__init__()

        self.__min = None
        self.__max = None

        # Can only specify one of bin_width and num_bins
        if (bin_width is None) == (num_bins is None):
            raise ValueError("Must specify only one of bin_width and num_bins")

        self._num_bins: Optional[int] = num_bins
        self._bin_width: Optional[Real] = bin_width

    def _find_min_max(self, items: Tuple[Binnable[Real], ...]) -> Tuple[Real, Real]:
        """
        Finds the minimum and maximum bin key value for the given items.

        :param items:   The binnable items.
        :return:        The min and max bin-key.
        """
        minimum = maximum = items[0].get_bin_key()

        for item in items[1:]:
            key = item.get_bin_key()
            minimum = min(minimum, key)
            maximum = max(maximum, key)

        return minimum, maximum

    def _configure(self, items: Tuple[Binnable[Real], ...]):
        # Find the min/max keys
        self.__min, self.__max = self._find_min_max(items)

        # Calculate the value that wasn't supplied explicitly
        if self._bin_width is None:
            self._bin_width = (self.__max - self.__min) / self._num_bins
        else:
            self._num_bins = ceil((self.__max - self.__min) / self._bin_width)

    def bin(self, item: Binnable[Real]) -> int:
        # Get the key for this item
        key: Real = item.get_bin_key()

        # Can't handle keys outside our configured range
        if key > self.__max or key < self.__min:
            raise ValueError("Item key is outside configured range")

        # Calculate the bin that the key should go into
        bin_id: int = (key - self.__min) // self._bin_width

        # Cap the key in case of rounding/etc
        if bin_id >= self._num_bins:
            bin_id = self._num_bins - 1

        return bin_id
