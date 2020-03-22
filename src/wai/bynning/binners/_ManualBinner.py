from numbers import Real
from typing import Optional, Tuple, List

from .._Binnable import Binnable
from ._EqualWidthBinner import EqualWidthBinner


class ManualBinner(EqualWidthBinner):
    """
    Equal-width binner which manually specifies the min/max bin-key,
    along with the number of bins/bin width.
    """
    def __init__(self,
                 min: Real,
                 max: Real,
                 *,
                 num_bins: Optional[int] = None, bin_width: Optional[Real] = None):
        super().__init__(num_bins=num_bins, bin_width=bin_width)

        self._min: Real = min
        self._max: Real = max

    def _find_min_max(self, items: List[Binnable[Real]]) -> Tuple[Real, Real]:
        return self._min, self._max
