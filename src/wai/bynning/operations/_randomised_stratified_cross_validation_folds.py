from random import Random
from typing import TypeVar, Iterable, Optional, List, Tuple, Iterator

from wai.common.iterate import random

from .._BinItem import BinItem
from .._Binning import Binning
from ..binners import StratifyingBinner, CrossValidationFoldBinner
from ..extraction import IndexExtractor

T = TypeVar("T")


def randomised_stratified_cross_validation_folds(items: Iterable[T],
                                                 num_folds: int,
                                                 rand: Optional[Random] = None) \
        -> Iterator[Tuple[Iterator[T], Iterator[T]]]:
    """
    Creates randomised stratified cross-validation folds from a set of data.

    :param items:       The items to create train/test folds for.
    :param num_folds:   The number of folds to create.
    :param rand:        An optional source of randomness.
    :return:            A list of folds, each containing a train/test pair
                        of lists of items in the folds.
    """
    # Wrap the items into bin-items
    bin_items: Iterator[BinItem[int, T]] = BinItem.extract_from(IndexExtractor[T](), items)

    # Randomise the bin items
    random_bin_items: Iterator[BinItem[int, T]] = random(bin_items, rand)

    # Stratify
    stratified: Binning[BinItem[int, T], int] = StratifyingBinner[T, int](num_folds).bin(random_bin_items)

    # Create the cross-validation folds
    fold_binnings: List[Binning[BinItem[int, T], str]] = \
        CrossValidationFoldBinner[int](num_folds).bin_all_folds(stratified.item_iterator())

    # Return the folds
    return (
        tuple(
            BinItem[int, T].unwrapping_iterator(fold_binning[bin_label])
            for bin_label in [CrossValidationFoldBinner[int].TRAIN_BIN_LABEL,
                              CrossValidationFoldBinner[int].TEST_BIN_LABEL]
        )
        for fold_binning in fold_binnings
    )
