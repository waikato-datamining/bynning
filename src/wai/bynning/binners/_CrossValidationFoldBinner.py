from typing import Optional, Tuple

from .._Binnable import Binnable
from .._typing import LabelType
from .._typing import KeyType
from ._ConfiguredBinner import ConfiguredBinner


class CrossValidationFoldBinner(ConfiguredBinner[KeyType, str]):
    """
    Binner which creates train/test splits for cross validation.
    """
    # The bin labels for the train and test data
    TRAIN_BIN_LABEL: str = "train"
    TEST_BIN_LABEL: str = "test"

    def __init__(self, num_folds: Optional[int] = None):
        # Must have at least 2 folds
        if num_folds is not None and num_folds < 2:
            raise ValueError(f"Must specify at least 2 folds, got {num_folds}")

        super().__init__()

        self._num_folds: Optional[int] = num_folds

        # Configured state
        self.__num_items: int = 0
        self.__fold_size: int = 0
        self.__num_big_folds: int = 0

        # Per-fold state
        self.__fold: int = 0
        self.__test_start_index: int = 0
        self.__test_end_index: int = 0

        # Per-item state
        self.__last_index: int = -1

    def _configure(self, items: Tuple[Binnable[KeyType], ...]):
        # Record the number of items
        self.__num_items = len(items)

        # Default to leave-one-out
        if self._num_folds is None:
            self._num_folds = self.__num_items
        # Must be more items than there are folds
        elif self._num_folds > self.__num_items:
            raise ValueError(f"{self._num_folds} requested but only {self.__num_items} provided")

        # Calculate the size of each fold
        self.__fold_size = self.__num_items // self._num_folds

        # Calculate the number of folds with one extra item
        self.__num_big_folds = self.__num_items % self._num_folds

        # Start at fold 0
        self.set_fold(0)

    def set_fold(self, fold: int):
        """
        Sets the fold number to bin against.

        :param fold:    The fold number.
        """
        # Can't go outside the range [0, num_folds)
        if fold < 0 or fold >= self._num_folds:
            raise ValueError(f"Fold must be in [0,{self._num_folds}), got {fold}")

        # Set the fold number
        self.__fold = fold

        # Calculate the start and end indices of the test set
        self.__test_start_index = self.__fold_size * fold + min(self.__num_big_folds, fold)
        self.__test_end_index = self.__test_start_index + self.__fold_size
        if fold < self.__num_big_folds:
            self.__test_end_index += 1

        # Reset the binning index
        self.__last_index = -1

    def bin(self, item: Binnable[KeyType]) -> LabelType:
        # Move to the next item index
        self.__last_index += 1

        # Put the item in the test or train set
        if self.__test_start_index <= self.__last_index < self.__test_end_index:
            return CrossValidationFoldBinner.TEST_BIN_LABEL
        else:
            return CrossValidationFoldBinner.TRAIN_BIN_LABEL

    def __iter__(self):
        self.set_fold(0)
        while True:
            yield self

            if self.__fold == self._num_folds - 1:
                return

            self.set_fold(self.__fold + 1)
