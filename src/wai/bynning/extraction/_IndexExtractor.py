from ._Extractor import Extractor, InputType


class IndexExtractor(Extractor[InputType, int]):
    """
    Extractor which simply extracts an integer index for each item.
    """
    def __init__(self):
        # The index of the next item
        self._index: int = 0

    def extract(self, item: InputType) -> int:
        # Get the index of this item
        index = self._index

        # Update the index for the next item
        self._index += 1

        return index
