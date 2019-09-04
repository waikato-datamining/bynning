from typing import Iterable, TypeVar, Iterator

from .._Binning import Binning
from .._BinItem import BinItem
from ..binners import StratifyingBinner
from ..extract import IdentityExtractor

T = TypeVar("T")


def stratify(num_folds: int, items: Iterable[T]) -> Iterator[T]:
    # Wrap the items in a bin-item
    bin_items = BinItem.extract_from(IdentityExtractor(), items)

    # Perform startified binning on the bin-items
    stratified_binning = Binning(StratifyingBinner(num_folds), bin_items)

    # Return the iterator over the original items in their new order
    return BinItem.unwrapping_iterator(stratified_binning.item_iterator())
