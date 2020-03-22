from random import Random, randrange as default_randrange
from typing import Optional, Dict

from ..extraction import Extractor, IdentityExtractor
from .._typing import KeyType, LabelType
from ._Binner import Binner


class RandomBinner(Binner[KeyType, LabelType]):
    """
    Binner which bins items randomly into a set number of bins.
    """
    def __init__(self,
                 num_bins: int,
                 label_extractor: Extractor[int, LabelType] = IdentityExtractor(),
                 rand: Optional[Random] = None):
        self._num_bins: int = num_bins
        self._labels: Dict[int, LabelType] = {index: label_extractor.extract(index)
                                              for index in range(num_bins)}
        self._randrange = rand.randrange if rand is not None else default_randrange

    def _bin(self, key: KeyType) -> LabelType:
        return self._labels[self._randrange(self._num_bins)]
