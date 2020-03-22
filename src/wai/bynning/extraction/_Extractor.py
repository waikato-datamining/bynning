from abc import abstractmethod
from typing import Generic, Iterator, Iterable, TypeVar

InputType = TypeVar("InputType")
OutputType = TypeVar("OutputType")


class Extractor(Generic[InputType, OutputType]):
    """
    Interface for classes which extract data of one type from data of another type.
    """
    @abstractmethod
    def extract(self, item: InputType) -> OutputType:
        """
        Extracts data from a given object.

        :param item:    The object to extract from.
        :return:        The extracted data.
        """
        pass

    def extract_all(self, items: Iterable[InputType]) -> Iterator[OutputType]:
        """
        Extracts data from all the given items.

        :param items:   The items to extract from.
        :return:        An iterator of extracted data.
        """
        return map(self.extract, items)
