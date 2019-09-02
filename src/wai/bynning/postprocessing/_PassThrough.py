from ._BinningPostProcessor import BinningPostProcessor
from .._Binning import Binning
from .._typing import LabelType, ItemType


class PassThrough(BinningPostProcessor[LabelType, ItemType]):
    """
    Does no post-processing.
    """
    def post_process_binning(self, binning: Binning[LabelType, ItemType]) -> Binning[LabelType, ItemType]:
        return binning
