from typing import List

from .._Binnable import Binnable
from ._TwoPassBinner import TwoPassBinner


class MinSizeBinner(TwoPassBinner[int, int]):
    """
    Binner which bins items by their size, placing items in
    indexed bins until they exceed a certain minimum total
    size.
    """
    def __init__(self, min_size: int):
        # Minimum size must be positive
        if min_size < 1:
            raise ValueError(f"Min size of bins must be positive, got {min_size}")

        self.min_size: int = min_size

        self._bin_index: int = 0
        self._remaining_size: int = 0
        self._current_size: int = 0

    def _configure(self, items: List[Binnable[int]]):
        # Calculate the total size of all items
        self._remaining_size = sum(Binnable.map_bin_keys(items))

        # Check there is enough size available
        if self._remaining_size < self.min_size:
            raise ValueError(f"Not enough total size in given items ({self._remaining_size}) "
                             f"to meet minimum size requirement of {self.min_size}")

    def _reset(self):
        self._bin_index = 0
        self._current_size = 0

    def _bin(self, key: int) -> int:
        # Move to the next bin if the current bin is full and
        # we can guarantee to fill another bin
        if self._current_size >= self.min_size and self._remaining_size >= self.min_size:
            self._bin_index += 1
            self._current_size = 0

        # Update the sizes
        self._current_size += key
        self._remaining_size -= key

        return self._bin_index
