from ._BinningPostProcessor import BinningPostProcessor
from .._Binning import Binning
from .._typing import LabelType, ItemType


class PassThrough(BinningPostProcessor[ItemType, LabelType]):
    """
    Does no post-processing.
    """
    def post_process_binning(self, binning: Binning[ItemType, LabelType]) -> Binning[ItemType, LabelType]:
        return binning
