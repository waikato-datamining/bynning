from ._Extractor import Extractor, InputType, OutputType


class ConstantExtractor(Extractor[InputType, OutputType]):
    """
    Extractor which extracts the same, given value for all input.
    """
    def __init__(self, constant: OutputType):
        self._constant: OutputType = constant

    def extract(self, item: InputType) -> OutputType:
        return self._constant
