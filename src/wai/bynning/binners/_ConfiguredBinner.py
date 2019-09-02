from abc import ABC, abstractmethod
from typing import Iterator, Iterable, Tuple

from .._Binnable import Binnable
from ._Binner import Binner
from .._typing import KeyType, LabelType


class ConfiguredBinner(Binner[KeyType, LabelType], ABC):
    """
    Class for binners which require an initial pass over
    the set of items being binned to generate state (e.g.
    statistics).
    """
    def __init__(self):
        self.__configured: bool = False

    def bin_all(self, items: Iterable[Binnable[KeyType]]) -> Iterator[Tuple[Binnable[KeyType], LabelType]]:
        # Configure ourselves on the items first
        if not self.__configured:
            items = self.configure(items)

        return super().bin_all(items)

    def configure(self, items: Iterable[Binnable[KeyType]]) -> Tuple[Binnable[KeyType], ...]:
        """
        Configures this binner on the given binnables items.

        :param items:   The items to configure ourselves against.
        :return:        A frozen view of the items.
        """
        # Can't configure more than once
        if self.__configured:
            raise RuntimeError("Cannot reconfigure binner")

        # Freeze the items
        items = tuple(items)

        # Can't configure on nothing
        if len(items) == 0:
            raise ValueError("No items provided for configuration")

        # Implement custom configuration
        self._configure(items)

        # Mark ourselves as configured
        self.__configured = True

        return items

    @abstractmethod
    def _configure(self, items: Tuple[Binnable[KeyType], ...]):
        """
        Configures this binner on the given binnables items.

        :param items:   The items to configure ourselves against.
        """
        pass

    def __getattribute__(self, item):
        # Can't get the "bin" method until we're configured
        if item == "bin" and not self.__configured:
            raise RuntimeError("Attempted to bin before configured")

        return super().__getattribute__(item)
