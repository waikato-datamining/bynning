from typing import Optional, Tuple

from wai.common import InvalidStateError

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

        self._fold: int = 0
        self._num_folds: Optional[int] = num_folds

        self.__num_items: int = 0
        self.__test_start_index: int = 0
        self.__test_end_index: int = 0
        self.__last_index: int = -1

    def next_fold(self) -> int:
        """
        Moves this cross-validation fold binner onto the next fold.

        :return:    The index of the next fold (0-based).
        """
        # Move to the next fold
        self._fold += 1

        # If we've moved past the last fold, raise
        if self._fold >= self._num_folds:
            raise InvalidStateError(f"Attempted to move to invalid fold {self._fold} (folds = {self._num_folds})")

        # Calculate the start and end index of the next test set
        test_start_index: int = self.__test_end_index
        test_end_index: int = test_start_index + (self.__test_end_index - self.__test_start_index)
        if self._fold == self.__num_items % self._num_folds:
            test_end_index -= 1
        self.__test_start_index = test_start_index
        self.__test_end_index = test_end_index

        # Reset the item index
        self.__last_index = -1

        return self._fold

    def _configure(self, items: Tuple[Binnable[KeyType], ...]):
        # Record the number of items
        self.__num_items = len(items)

        # Default to leave-one-out
        if self._num_folds is None:
            self._num_folds = self.__num_items
        # Must be more items than there are folds
        elif self._num_folds > self.__num_items:
            raise ValueError(f"{self._num_folds} requested but only {self.__num_items} provided")

        # Calculate the size of the test-set
        self.__test_end_index = self.__num_items // self._num_folds
        if self.__num_items % self._num_folds != 0:
            self.__test_end_index += 1

    def bin(self, item: Binnable[KeyType]) -> LabelType:
        # Move to the next item index
        self.__last_index += 1

        # Put the item in the test or train set
        if self.__test_start_index <= self.__last_index < self.__test_end_index:
            return TEST_BIN_LABEL
        else:
            return TRAIN_BIN_LABEL

    def __iter__(self):
        return self

    def __next__(self):
        if self._fold < self._num_folds - 1:
            self.next_fold()
            return self
        else:
            raise StopIteration
