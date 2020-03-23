from typing import Tuple

from wai.common.number import Rational


def integer_dot_product(a: Tuple[int], b: Tuple[int]) -> Rational:
    """
    Calculates the square of the dot-product between to vectors
    of integers.

    :param a:   The first integer vector.
    :param b:   The second integer vector.
    :return:    The square of the dot-product.
    """
    # Make sure the vectors are the same length
    if len(a) != len(b):
        raise ValueError(f"Can't perform integer dot product between vectors of different "
                         f"lengths: {a}, {b}")

    return Rational(
        sum(a_i * b_i for a_i, b_i in zip(a, b)) ** 2,
        sum(a_i ** 2 for a_i in a) * sum(b_i ** 2 for b_i in b)
    )
