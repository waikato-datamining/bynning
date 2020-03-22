from typing import TypeVar, Iterator, Iterable

from .._BinItem import BinItem
from .._Binning import Binning
from ..binners import MinSizeBinner
from ..extraction import ConstantExtractor

T = TypeVar("T")


def group(size: int, items: Iterable[T]) -> Iterator[Iterator[T]]:
    """
    Groups the items into a number of iterators of at least a certain size.

    :param size:    The minimum size for each iterator.
    :param items:   The items to group.
    :return:        An iterator over the group iterators.
    """
    # Wrap the items in bin-items all with size 1
    bin_items: Iterator[BinItem[int, T]] = \
        BinItem[int, T].extract_from(ConstantExtractor[T, int](1), items)

    # Perform min-size binning
    binning: Binning[BinItem[int, T], int] = MinSizeBinner(size).bin(bin_items)

    # Return the iterator over the original items in their new order
    return (BinItem.unwrapping_iterator(bin) for bin in binning)
