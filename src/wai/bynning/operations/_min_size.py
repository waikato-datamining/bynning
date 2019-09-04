from .._Binning import Binning
from .._typing import ItemType, LabelType
from ..binners import MinSizeBinner
from ..extract import SizeExtractor


def min_size(size: int, binning: Binning[ItemType, LabelType]) -> Binning[ItemType, int]:
    """
    Returns a binning with at least the given number of items in each bin.
    The ordering of items is maintained, but the original bin labels are lost.

    :param size:        The minimum number of items to place in each bin.
    :param binning:     The binning to process.
    :return:            A new binning with the constraint met.
    """
    return binning.rebin(MinSizeBinner(size), SizeExtractor(), True)
