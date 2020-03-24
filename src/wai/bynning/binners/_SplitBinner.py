from fractions import Fraction
from typing import Tuple, List

from ..extraction import Extractor, IdentityExtractor
from ..util import integer_dot_product
from .._typing import KeyType, LabelType
from ._Binner import Binner


class SplitBinner(Binner[KeyType, LabelType]):
    """
    Binner which proportionately splits items into bins based on
    a selected ratio of bin-sizes.
    """
    def __init__(self, *ratios: int, label_extractor: Extractor[int, LabelType] = IdentityExtractor()):
        # Must provide at least 1 ratio values
        if len(ratios) == 0:
            raise ValueError("No ratios provided")

        # Make sure the ratios are non-negative
        if any(ratio < 0 for ratio in ratios):
            raise ValueError(f"Ratios must be non-negative, got {ratios}")

        # Must have at least 1 positive ratio
        if all(ratio == 0 for ratio in ratios):
            raise ValueError(f"Must have at least one non-zero ratio")

        # The schedule of labels to return
        self._schedule: List[LabelType] = list(label_extractor.extract_all(self._calculate_schedule(ratios)))

        # The current position in the schedule
        self._schedule_index: int = 0

    def _reset(self):
        self._schedule_index = 0

    def _bin(self, key: KeyType) -> LabelType:
        # Get the next label from the schedule
        label = self._schedule[self._schedule_index]

        # Move to the next label in the schedule
        self._schedule_index = (self._schedule_index + 1) % len(self._schedule)

        return label

    @staticmethod
    def _calculate_schedule(ratios: Tuple[int]) -> List[int]:
        """
        Calculates the schedule of labels to return to best split
        items into the bins.

        :return:    The label schedule.
        """
        # Initialise an empty schedule
        schedule: List[int] = []

        # The initial best candidate binning is all bins empty
        best_candidate: Tuple[int] = tuple(0 for _ in range(len(ratios)))

        # The schedule cycle-length is the sum of ratios
        for schedule_index in range(sum(ratios)):
            # Create a candidate ratio for each of the possible binnings
            # (each being a single item added to one of the bins)
            candidate_ratios: Tuple[Tuple[int, ...]] = tuple(
                tuple(ratio + 1 if i == candidate_index else ratio
                      for i, ratio in enumerate(best_candidate))
                for candidate_index in range(len(ratios))
            )

            # Calculate the integer dot-product of each candidate ratio
            # to determine which is closest to the desired ratio
            candidate_dps: Tuple[Fraction, ...] = tuple(
                integer_dot_product(ratios, candidate_ratio)
                for candidate_ratio in candidate_ratios
            )

            # Select the candidate with the best (greatest) dot-product
            best_candidate_index = None
            best_candidate_dp = None
            for candidate_index, candidate_dp in enumerate(candidate_dps):
                if best_candidate_index is None or candidate_dp > best_candidate_dp:
                    best_candidate = candidate_ratios[candidate_index]
                    best_candidate_index = candidate_index
                    best_candidate_dp = candidate_dp

            # Add the selected candidate bin to the schedule
            schedule.append(best_candidate_index)

        return schedule
