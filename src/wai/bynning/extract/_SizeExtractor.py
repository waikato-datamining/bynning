from typing import Sized

from ._Extractor import Extractor


class SizeExtractor(Extractor[Sized, int]):
    """
    Extractor which extracts the size of the given item using len().
    """
    def extract(self, item: Sized) -> int:
        return len(item)
