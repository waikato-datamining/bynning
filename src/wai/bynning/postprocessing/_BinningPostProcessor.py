from abc import abstractmethod
from typing import Generic

from .._Binning import Binning
from .._typing import LabelType, ItemType


class BinningPostProcessor(Generic[LabelType, ItemType]):
    @abstractmethod
    def post_process_binning(self, binning: Binning[LabelType, ItemType]) -> Binning[LabelType, ItemType]:
        """
        Applies the post-processing of this scheme to the
        given binning.

        :param binning:     The binning to post-process.
        :return:            The post-processed binning.
        """
        pass
