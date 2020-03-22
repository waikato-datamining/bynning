from typing import Dict

from ..extraction import Extractor, IdentityExtractor
from .._typing import KeyType, LabelType
from ._Binner import Binner


class StratifyingBinner(Binner[KeyType, LabelType]):
    """
    Binner which cyclically stratifies items over a number of bins.
    """
    def __init__(self,
                 num_folds: int,
                 label_extractor: Extractor[int, LabelType] = IdentityExtractor()):
        self._num_folds: int = num_folds
        self._labels: Dict[int, LabelType] = {index: label_extractor.extract(index)
                                              for index in range(self._num_folds)}
        self._next: int = 0

    def _reset(self):
        self._next = 0

    def _bin(self, key: KeyType) -> LabelType:
        # Get the next stratification label to use
        label: int = self._next

        # Increment the next label
        self._next += 1
        self._next %= self._num_folds

        return self._labels[label]
