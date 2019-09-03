from .._Binnable import Binnable
from ._Binner import Binner
from .._typing import KeyType, LabelType
from ..extract import Extractor


class ArbitraryBinner(Binner[KeyType, LabelType]):
    """
    Binner which bins items into arbitrary bins using an extractor
    to specify the label.
    """
    def __init__(self, label_extractor: Extractor[KeyType, LabelType]):
        self.__label_extractor: Extractor[KeyType, LabelType] = label_extractor

    def bin(self, item: Binnable[KeyType]) -> LabelType:
        return self.__label_extractor.extract(item.get_bin_key())
