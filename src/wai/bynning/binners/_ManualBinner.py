from numbers import Real
from typing import Optional, Tuple

from .._Binnable import Binnable
from ._EqualWidthBinner import EqualWidthBinner


class ManualBinner(EqualWidthBinner):
    """
    Equal-width binner which manually specifies the min/max bin-key,
    along with the number of bins/bin width.
    """
    def __init__(self, min_: Real, max_: Real,
                 *,
                 num_bins: Optional[int] = None, bin_width: Optional[Real] = None):
        super().__init__(num_bins=num_bins, bin_width=bin_width)

        self.__min: Real = min_
        self.__max: Real = max_

    def _find_min_max(self, items: Tuple[Binnable[Real], ...]) -> Tuple[Real, Real]:
        return self.__min, self.__max
