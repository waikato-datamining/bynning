from numbers import Real
from typing import Tuple

from wai.common.statistics import interquartile_range

from .._Binnable import Binnable
from ._EqualWidthBinner import EqualWidthBinner


class FreedmanDiaconisChoiceBinning(EqualWidthBinner):
    """
    The Freedman-Diaconis' choice is based on the interquartile range. It
    replaces 3.5σ of Scott's rule with 2 IQR, which is less sensitive than
    the standard deviation to outliers in data.
    """
    def __init__(self):
        # Doesn't matter how many bins we set here as it is overridden
        # in _configure
        super().__init__(bin_width=1)

    def _configure(self, items: Tuple[Binnable[Real], ...]):
        iqr: Real = interquartile_range(map(Binnable.get_bin_key, items))
        self._bin_width = (2 * iqr) / (len(items) ** (1/3))

        super()._configure(items)
