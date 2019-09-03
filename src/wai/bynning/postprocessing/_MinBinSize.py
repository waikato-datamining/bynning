from typing import List

from ._BinningPostProcessor import BinningPostProcessor
from .._Binning import Binning
from .._Bin import Bin
from .._typing import ItemType, KeyType


class MinBinSize(BinningPostProcessor[ItemType, int]):
    """
    Merges bins in a binning until all bins are of at least a certain
    size. Assumes the bin labels are indexes.
    """
    def __init__(self, min_size: int):
        self._min_size: int = min_size

    def post_process_binning(self, binning: Binning[ItemType, int]) -> Binning[ItemType, int]:
        # If the constraint can't be satisfied, raise
        total_num_items: int = sum(map(len, binning))
        if total_num_items < self._min_size:
            raise ValueError(f"Minimum bin size is {self._min_size} but given "
                             f"binning only contains {total_num_items} items")

        # Create a list to hold the new bins
        new_bins: List[Bin[ItemType, int]] = [Bin(0)]

        # Process each bin in turn
        for bin in binning:
            # Get the next bin to fill up
            new_bin: Bin[ItemType, int] = new_bins[-1]

            # If the bin is already full enough, create a new bin
            if len(new_bin) >= self._min_size:
                new_bin = Bin(len(new_bins))
                new_bins.append(new_bin)

            # Add the items from the original bin to the new bin
            new_bin.merge(bin)

        # Create a new binning
        new_binning: Binning[ItemType, int] = Binning(binning._binner)
        new_binning._bins = {index: bin for index, bin in enumerate(new_bins)}

        return new_binning
