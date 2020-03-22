from ._Binner import Binner
from .._typing import KeyType, LabelType, ItemType
from ..extraction import Extractor


class ArbitraryBinner(Binner[KeyType, LabelType]):
    """
    Binner which bins items into arbitrary bins using an extractor
    to specify the label.
    """
    def __init__(self, label_extractor: Extractor[KeyType, LabelType]):
        self._label_extractor: Extractor[KeyType, LabelType] = label_extractor

    def _bin(self, item: ItemType) -> LabelType:
        return self._label_extractor.extract(item.bin_key)
