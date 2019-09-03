from .._Binnable import Binnable
from ._Binner import Binner
from .._typing import KeyType, LabelType
from .._Extractor import Extractor


class GroupingBinner(Binner[KeyType, LabelType]):
    """
    Binner which bins items into arbitrary groups using an extractor.
    """
    def __init__(self, group_extractor: Extractor[KeyType, LabelType]):
        self.__group_extractor: Extractor[KeyType, LabelType] = group_extractor

    def bin(self, item: Binnable[KeyType]) -> LabelType:
        return self.__group_extractor.extract(item.get_bin_key())
