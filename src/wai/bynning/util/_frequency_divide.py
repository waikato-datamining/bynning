

def frequency_divide(total_size: int,
                     num_segments: int,
                     segment: int) -> range:
    """
    Divides a number of items into a number of segments,
    where each segment has the same number of items. If the
    number of items doesn't divide evenly, each of the first
    N (== total_size % num_segments) segments will have one extra
    item each.

    :param total_size:      The total number of items to segment.
    :param num_segments:    The total number of segments to produce.
    :param segment:         The index of the segment to return.
    :return:                The range of item indices for the selected segment.
    """
    # Make sure there is at least one item to segment
    if total_size < 1:
        raise ValueError(f"Can't divide a non-positive number of items, got {total_size}")

    # Make sure there is at least one segment
    if num_segments < 1:
        raise ValueError(f"Can't create a non-negative number of segments, got {num_segments}")

    # Normalise the segment index
    segment = range(num_segments)[segment]

    # Calculate the size of each segment
    segment_size = total_size // num_segments

    # Calculate the number of segments with one extra item
    num_big_segments = total_size % num_segments

    # Calculate the start index of the selected segment
    test_start_index = segment_size * segment + min(num_big_segments, segment)

    return range(
        test_start_index,
        test_start_index + segment_size + (1 if segment < num_big_segments else 0)
    )
