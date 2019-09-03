from typing import Tuple, List

from .._Binnable import Binnable
from .._typing import LabelType
from ._ConfiguredBinner import ConfiguredBinner


class MinSizeBinner(ConfiguredBinner[int, int]):
    """
    Binner which bins items by their size, placing items in
    indexed bins until they exceed a certain minimum total
    size.
    """
    def __init__(self, min_size: int):
        super().__init__()

        self.min_size: int = min_size
        self._allocations: List[int] = []
        self._allocation: int = 0
        self._last_index: int = -1

    def _configure(self, items: Tuple[Binnable[int], ...]):
        # Allocate items to bins in order until full
        current_size: int = 0
        for index, item in enumerate(items):
            # Keep track of the bin's size
            current_size += item.get_bin_key()

            # Move to the next bin once this one is full
            if current_size >= self.min_size:
                self._allocations.append(index + 1)
                current_size = 0

        # If we didn't fill up bin 0, there wasn't enough size available
        if len(self._allocations) == 0:
            raise ValueError(f"Not enough total size in given items to "
                             f"meet minimum size requirement of {self.min_size}")

        # If the current size of the last bin is too small, back allocate
        # those items to the previous bin
        if current_size != 0:
            self._allocations.pop()

    def bin(self, item: Binnable[int]) -> LabelType:
        # Keep a stateful enumeration of items
        self._last_index += 1

        # Move to the next allocation if we've filled the bin
        if self._allocations[self._allocation] == self._last_index:
            self._allocation += 1

        # Return the bin allocation for this item
        return self._allocation
