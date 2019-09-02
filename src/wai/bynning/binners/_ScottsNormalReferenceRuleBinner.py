from numbers import Real
from statistics import stdev
from typing import Tuple

from .._Binnable import Binnable
from ._EqualWidthBinner import EqualWidthBinner


class ScottsNormalReferenceRuleBinner(EqualWidthBinner):
    """
    Scott's normal reference rule is optimal for random samples of normally
    distributed data, in the sense that it minimizes the integrated mean
    squared error of the density estimate.
    """
    def __init__(self):
        # Doesn't matter how many bins we set here as it is overridden
        # in _configure
        super().__init__(bin_width=1)

    def _configure(self, items: Tuple[Binnable[Real], ...]):
        standard_deviation: float = stdev(map(float, map(Binnable.get_bin_key, items)))
        self._bin_width = (3.5 * standard_deviation) / (len(items) ** (1/3))

        super()._configure(items)
