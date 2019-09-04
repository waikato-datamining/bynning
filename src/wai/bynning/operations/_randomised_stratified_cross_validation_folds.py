from random import Random
from typing import TypeVar, Iterable, Optional, List, Tuple, Iterator

from wai.common.iterate import random

from .._BinItem import BinItem
from .._Binning import Binning
from ..binners import StratifyingBinner, CrossValidationFoldBinner
from ..extract import IdentityExtractor

T = TypeVar("T")


def randomised_stratified_cross_validation_folds(items: Iterable[T],
                                                 num_folds: int,
                                                 rand: Optional[Random] = None) -> List[Tuple[List[T]]]:
    """
    Creates randomised stratified cross-validation folds from a set of data.

    :param items:       The items to create train/test folds for.
    :param num_folds:   The number of folds to create.
    :param rand:        An optional source of randomness.
    :return:            A list of folds, each containing a train/test pair
                        of lists of items in the folds.
    """
    # Wrap the items into bin-items
    bin_items: Iterator[BinItem[T, T]] = BinItem.extract_from(IdentityExtractor(), items)

    # Randomise the bin items
    random_bin_items: Iterator[BinItem[T, T]] = random(bin_items, rand)

    # Stratify
    binning: Binning[BinItem[T, T], int] = Binning(StratifyingBinner[T, int](num_folds), random_bin_items)

    # Create the cross-validation folds
    fold_binnings: List[Binning[BinItem[T, T], str]] = [binning.rebin(fold_binner)
                                                        for fold_binner in CrossValidationFoldBinner(num_folds)]

    # Return the folds
    return list(
        tuple(
            list(
                BinItem.unwrapping_iterator(fold[bin_label])
            )
            for bin_label in [CrossValidationFoldBinner.TRAIN_BIN_LABEL, CrossValidationFoldBinner.TEST_BIN_LABEL]
        )
        for fold in fold_binnings
    )
