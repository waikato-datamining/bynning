from typing import Optional, Iterable, List

from ..util import conservatively_cache, frequency_divide
from .._Binning import Binning
from .._typing import KeyType, ItemType
from ._TwoPassBinner import TwoPassBinner


class CrossValidationFoldBinner(TwoPassBinner[KeyType, str]):
    """
    Binner which creates train/test splits for cross validation.
    """
    # The bin labels for the train and test data
    TRAIN_BIN_LABEL: str = "train"
    TEST_BIN_LABEL: str = "test"

    def __init__(self, num_folds: Optional[int] = None, fold: int = 0):
        # Must have at least 2 folds
        if num_folds is not None and num_folds < 2:
            raise ValueError(f"Must specify at least 2 folds, got {num_folds}")

        self._num_folds: Optional[int] = num_folds
        self._fold: int = fold
        self._test_range: range = range(0)
        self._item_index: int = 0

    def _configure(self, items: List[ItemType]):
        # Record the number of items
        num_items = len(items)

        # Default to leave-one-out
        if self._num_folds is None:
            self._num_folds = num_items
            self._fold = self._fold % num_items
        # Must be more items than there are folds
        elif self._num_folds > num_items:
            raise ValueError(f"{self._num_folds} requested but only {num_items} provided")

        # Calculate the index range of the test items
        self._test_range = frequency_divide(num_items, self._num_folds, self._fold)

    def _reset(self):
        self._item_index = 0

    def _bin(self, key: KeyType) -> str:
        # Determine if the item is in the train or test set
        label = (
            CrossValidationFoldBinner.TEST_BIN_LABEL
            if self._item_index in self._test_range else
            CrossValidationFoldBinner.TRAIN_BIN_LABEL
        )

        # Move to the next item index
        self._item_index += 1

        return label

    def next_fold(self):
        """
        Sets the 'fold' value to the one after its current value
        (goes back to fold 0 if on the last fold).
        """
        self._fold += 1
        if self._num_folds is not None:
            self._fold %= self._num_folds

    def set_fold(self, fold: int):
        """
        Sets the fold number to bin against.

        :param fold:    The fold number.
        """
        # Can't go outside the range [0, num_folds)
        if self._num_folds is not None and fold not in range(self._num_folds):
            raise ValueError(f"Fold must be in [0,{self._num_folds}), got {fold}")

        # Set the fold number
        self._fold = fold

    def bin_all_folds(self, items: Iterable[ItemType]) -> List[Binning[ItemType, str]]:
        """
        Creates a binning for each cross-validation fold of the items.

        :param items:   The items to bin.
        :return:        A binning for each fold.
        """
        # Make sure we can iterate through items multiple times
        items = conservatively_cache(items)

        # Create an empty list to hold the binnings
        binnings = []

        # Save the state of the binner so it can be restored afterwards
        saved_state = self._fold, self._num_folds

        # Go to fold zero
        self.set_fold(0)

        # Create a binning for each fold
        while len(binnings) == 0 or self._fold != 0:
            binnings.append(self.bin(items))
            self.next_fold()

        # Restore the saved state
        self._fold, self._num_folds = saved_state

        return binnings
