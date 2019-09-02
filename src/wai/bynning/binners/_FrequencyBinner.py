from numbers import Real
from typing import List, Dict, Tuple

from .._Binnable import Binnable
from ._ConfiguredBinner import ConfiguredBinner


class FrequencyBinner(ConfiguredBinner[Real, int]):
    def __init__(self, num_bins: int):
        super().__init__()

        if num_bins < 1:
            raise ValueError("Must specify at least one bin")

        self.__num_bins: int = num_bins
        self.__lookup: Dict[Binnable[Real], int] = {}

    def _configure(self, items: Tuple[Binnable[Real], ...]):
        # Sort the items by their key
        item_list: List[Binnable[Real]] = list(items)
        item_list.sort(key=lambda x: x.get_bin_key())

        # Calculate the number of items in each bin
        num_items: int = len(item_list)
        bin_size: int = num_items // self.__num_bins
        num_big_bins: int = num_items % self.__num_bins

        # Create lookup-sets of items for each bin
        item_index: int = 0
        for bin_index in range(self.__num_bins):
            for _ in range(bin_size + 1 if bin_index < num_big_bins else bin_size):
                self.__lookup[item_list[item_index]] = bin_index
                item_index += 1

    def bin(self, item: Binnable[Real]) -> int:
        if item not in self.__lookup:
            raise ValueError("Cannot bin item not seen during configuration")

        return self.__lookup[item]
