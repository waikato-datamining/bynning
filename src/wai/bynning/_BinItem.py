from typing import Generic, Iterator, Iterable, TypeVar

from ._typing import KeyType
from ._Binnable import Binnable
from .extract import Extractor

PayloadType = TypeVar("PayloadType")  # The type of the payload of the bin-item (generally non-binnable)


class BinItem(Binnable[KeyType], Generic[KeyType, PayloadType]):
    """
    Wrapper class for objects which makes them binnable. Also provides the capability
    of respecifying the bin-key of another binnable, by wrapping it in this class with
    an extractor.
    """
    def __init__(self, key: KeyType, item: PayloadType):
        self._key: KeyType = key
        self._payload: PayloadType = item

    def get_bin_key(self) -> KeyType:
        return self._key

    def payload(self) -> PayloadType:
        """
        Gets the item that is the payload for this bin item.
        """
        return self._payload

    def payload_is_binnable(self) -> bool:
        """
        Checks if the payload of this bin-item is binnable (i.e. this
        bin-item is being used to modify the bin-key of the payload).
        """
        return isinstance(self._payload, Binnable)

    def __str__(self) -> str:
        return str(self._key) + ":" + str(self._payload)

    @staticmethod
    def extract_from(extractor: Extractor[PayloadType, KeyType], items: Iterable[PayloadType]) \
            -> Iterator['BinItem[KeyType, PayloadType]']:
        """
        Extracts a bin-item from each given item using the given key-extractor.

        :param extractor:   The extractor to use to extract the bin key.
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
        return map(BinItem.payload, wrapped_iterator)
