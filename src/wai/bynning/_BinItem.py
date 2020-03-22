from typing import Generic, Iterator, Iterable, TypeVar

from ._typing import KeyType
from ._Binnable import Binnable
from .extraction import Extractor

# The type of the payload of the bin-item (generally non-binnable)
PayloadType = TypeVar("PayloadType")


class BinItem(Binnable[KeyType], Generic[KeyType, PayloadType]):
    """
    Wrapper class for objects which makes them binnable. Also provides the capability
    of respecifying the bin-key of another binnable, by wrapping it in this class with
    an extractor.
    """
    def __init__(self, bin_key: KeyType, item: PayloadType):
        self._bin_key: KeyType = bin_key
        self._payload: PayloadType = item

    @property
    def bin_key(self) -> KeyType:
        return self._bin_key

    @property
    def payload(self) -> PayloadType:
        """
        Gets the item that is the payload for this bin item.
        """
        return self._payload

    @property
    def payload_is_binnable(self) -> bool:
        """
        Checks if the payload of this bin-item is binnable (i.e. this
        bin-item is being used to modify the bin-key of the payload).
        """
        return isinstance(self._payload, Binnable)

    def __str__(self) -> str:
        return f"({self._bin_key}): {self._payload}"

    @staticmethod
    def extract_from(extractor: Extractor[PayloadType, KeyType],
                     items: Iterable[PayloadType]) -> Iterator['BinItem[KeyType, PayloadType]']:
        """
        Extracts a bin-item from each given item using the given key-extractor.

        :param extractor:   The extractor to use to extract the bin-key,
                            or a constant bin-key to use for all items.
        :param items:       The items to create bin-items for.
        :return:            The bin-items.
        """
        return (BinItem(extractor.extract(item), item) for item in items)

    @staticmethod
    def unwrapping_iterator(wrapped_iterator: Iterator['BinItem[KeyType, PayloadType]']) \
            -> Iterator[PayloadType]:
        """
        Returns an iterator over the payloads of the bin-items in the given iterator.

        :param wrapped_iterator:    An iterator over bin-items.
        """
        return (item.payload for item in wrapped_iterator)
