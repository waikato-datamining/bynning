from ._Binner import Binner
from .._typing import KeyType, LabelType


class NoBinner(Binner[KeyType, LabelType]):
    """
    Binner which performs no real binning, putting all
    items in a single bin with the given label.
    """
    def __init__(self, label: LabelType):
        self._label: LabelType = label

    def _bin(self, key: KeyType) -> LabelType:
        return self._label
