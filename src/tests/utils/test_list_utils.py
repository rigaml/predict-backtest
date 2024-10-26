import pytest

import utils.list_utils as list_utils


@pytest.mark.parametrize("indexes, expected", [
    # No duplication
    ([], [0, 1, 2, 3, 4]),
    # Duplicate element in first position
    ([0], [0, 1, 2, 3, 4, 0]),
    # Duplicate element in middle position
    ([3], [0, 1, 2, 3, 4, 3]),
    # Duplicate 2 elements
    ([0, 3], [0, 1, 2, 3, 4, 0, 3]),
    # Duplicate 4 elements
    ([0, 3, 3, 0], [0, 1, 2, 3, 4, 0, 3, 3, 0]),
])
def test_duplicate_values(indexes, expected):
    lst = [0, 1, 2, 3, 4]

    result = list_utils.duplicate_values(lst, indexes)

    assert result == expected


@pytest.mark.parametrize(
    "lst, indexes, expected",
    [
        # Empty indexes list with empty list
        ([], [], []),

        # Empty list
        ([], [0], []),

        # Single element list with index to remove
        ([1], [0], []),

        # Single element list with index not to remove
        ([1], [1], [1]),

        # No indexes to remove
        ([1, 2, 3], [], [1, 2, 3]),

        # Removing all but one element
        ([10, 20, 30, 40], [1, 2, 3], [10]),

        # Duplicate indexes should be handled
        ([1, 2, 3], [1, 1], [1, 3]),

        # Index out of range should be ignored
        ([1, 2, 3], [5], [1, 2, 3]),

        # All indexes are out of range
        ([1, 2, 3], [3, 4, 5], [1, 2, 3]),

        # Large list with multiple indexes to remove
        (list(range(100)), list(range(0, 100, 2)), list(range(1, 100, 2))),
    ]
)
def test_remove_indexes(lst, indexes, expected):
    assert list_utils.remove_indexes(lst, indexes) == expected


@pytest.mark.parametrize("data, start_slice, end_slice, expected", [
    # No slicing
    ([1, 2, 3, 4, 5], 0, 0, [1, 2, 3, 4, 5]),
    # Slicing from start
    ([1, 2, 3, 4, 5], 2, 0, [3, 4, 5]),
    # Slicing to end
    ([1, 2, 3, 4, 5], 0, 2, [1, 2, 3]),
    # Slicing from start and to end
    ([1, 2, 3, 4, 5], 1, 1, [2, 3, 4]),
    # Negative start_slice
    ([1, 2, 3, 4, 5], -1, 0, [1, 2, 3, 4, 5]),
    # Negative end_slice
    ([1, 2, 3, 4, 5], 0, -1, [1, 2, 3, 4, 5]),
    # Both negative
    ([1, 2, 3, 4, 5], -1, -1, [1, 2, 3, 4, 5]),
    # Empty list
    ([], 1, 1, []),
    # Start slice greater than length
    ([1, 2, 3, 4, 5], 10, 0, []),
    # End slice greater than length
    ([1, 2, 3, 4, 5], 0, 10, []),
])
def test_safe_slice(data, start_slice, end_slice, expected):
    assert list_utils.safe_slice(data, start_slice, end_slice) == expected
