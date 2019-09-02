from typing import Generic, Iterator, Iterable

from ._typing import KeyType, ItemType
from ._Binnable import Binnable
from ._BinKeyExtractor import BinKeyExtractor


class BinItem(Binnable[KeyType], Generic[KeyType, ItemType]):
    """
    Wrapper class for objects which makes them binnable.
    """
    def __init__(self, key: KeyType, item: ItemType):
        self._key: KeyType = key
        self._payload: ItemType = item

    def get_bin_key(self) -> KeyType:
        return self._key

    def payload(self) -> ItemType:
        """
        Gets the item that is the payload for this bin item.
        """
        return self._payload

    def __str__(self) -> str:
        return str(self._key) + ":" + str(self._payload)

    @staticmethod
    def extract_from(extractor: BinKeyExtractor[ItemType, KeyType], items: Iterable[ItemType]) \
            -> Iterator['BinItem[KeyType, ItemType]']:
        """
        Extracts a bin-item from each given item using the given key-extractor.

        :param extractor:   The extractor to ise to extract the bin key.
        :param items:       The items to create bin-items for.
        :return:            The bin-items.
        """
        return (BinItem(extractor.extract_bin_key(item), item) for item in items)
