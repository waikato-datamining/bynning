from random import Random
from typing import Iterable, TypeVar, Dict, Iterator, Optional

from wai.common.iterate import random

from ..binners import SplitBinner
from ..extraction import LabelExtractor, IndexExtractor
from .._BinItem import BinItem

T = TypeVar("T")


def split(items: Iterable[T], rand: Optional[Random] = None, **ratios: int) -> Dict[str, Iterator[T]]:
    """
    Splits the items into categories, with a certain proportion of
    the items going into each category.

    :param items:       The items to split.
    :param rand:        Optional RNG to randomise the split.
    :param ratios:      The category proportions, keyed by category name.
    :return:            A dictionary of category name to an iterator of the
                        items in that category.
    """
    # Extract the proportions and categories into separate lists,
    # ensuring the paired ordering is preserved
    ratio_list = []
    label_list = []
    for label, ratio in ratios.items():
        label_list.append(label)
        ratio_list.append(ratio)

    # Wrap the items in a bin-item
    bin_items: Iterator[BinItem[int, T]] = BinItem[int, T].extract_from(IndexExtractor[T](), items)

    # Optionally randomise the item order
    if rand is not None:
        bin_items = random(bin_items, rand)

    # Use the split-binner to perform the split, with a labeller
    binning = SplitBinner[int, str](*ratio_list, label_extractor=LabelExtractor[str](*label_list)).bin(bin_items)

    # Return the iterators over the original items in their split categories
    return {bin.label: BinItem.unwrapping_iterator(bin) for bin in binning}
