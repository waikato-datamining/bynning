from .._Binnable import Binnable
from ._Binner import Binner
from .._typing import KeyType, LabelType


class NoBinner(Binner[KeyType, LabelType]):
    """
    Binner which performs no real binning, putting all
    items in a single bin with the given label.
    """
    def __init__(self, label: LabelType):
        self.__label: LabelType = label

    def bin(self, item: Binnable[KeyType]) -> LabelType:
        return self.__label
