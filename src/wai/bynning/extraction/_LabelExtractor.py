from typing import Tuple

from .._typing import LabelType
from ._Extractor import Extractor


class LabelExtractor(Extractor[int, LabelType]):
    """
    Extractor which assigns a label to each index in
    a zero-based range.
    """
    def __init__(self, *labels: LabelType):
        # The labels to use
        self._labels: Tuple[LabelType, ...] = labels

    def extract(self, item: int) -> LabelType:
        return self._labels[item]
