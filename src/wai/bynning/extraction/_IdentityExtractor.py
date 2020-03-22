from ._Extractor import Extractor, InputType


class IdentityExtractor(Extractor[InputType, InputType]):
    """
    Extractor which returns the input.
    """
    def extract(self, item: InputType) -> InputType:
        return item
