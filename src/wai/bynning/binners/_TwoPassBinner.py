from abc import ABC, abstractmethod
from typing import Iterable, Tuple, Iterator, List

from .._typing import KeyType, LabelType, ItemType
from ._Binner import Binner


class TwoPassBinner(Binner[KeyType, LabelType], ABC):
    """
    Class for binners which require an initial pass over
    the set of items being binned to generate state (e.g.
    statistics).
    """
    def _bin_items(self, items: Iterable[ItemType]) -> Iterator[Tuple[LabelType, ItemType]]:
        # Need to cache the items as we're doing two passes
        items = list(items)

        # Configure ourselves on the items first
        self._configure(items)

        return super()._bin_items(items)

    @abstractmethod
    def _configure(self, items: List[ItemType]):
        """
        Configures this binner on the given binnables items. Can modify
        the items list as well.

        :param items:   The items to configure ourselves against.
        """
        pass
