from typing import Iterable, TypeVar, Iterator

from .._Binning import Binning
from .._BinItem import BinItem
from ..binners import StratifyingBinner
from ..extraction import IndexExtractor

T = TypeVar("T")


def stratify(num_strata: int, items: Iterable[T]) -> Iterator[T]:
    """
    Stratifies a series of items. Result is every nth item of
    the input, followed by every nth item + 1, nth + 2, etc.

    :param num_strata:  The number of strata to produce.
    :param items:       The items to stratify.
    :return:            An iterator over the items in stratified order.
    """
    # Wrap the items in a bin-item
    bin_items: Iterator[BinItem[int, T]] = BinItem[int, T].extract_from(IndexExtractor[T](), items)

    # Perform startified binning on the bin-items
    stratified_binning: Binning[BinItem[int, T], int] = StratifyingBinner[int, int](num_strata).bin(bin_items)

    # Return the iterator over the original items in their new order
    return BinItem.unwrapping_iterator(stratified_binning.item_iterator())
