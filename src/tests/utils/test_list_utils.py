import pytest

from src.utils.list_utils import duplicate_values


@pytest.mark.parametrize("indexes, expected", [
    ([], [0, 1, 2, 3, 4]),
    ([0], [0, 1, 2, 3, 4, 0]),
    ([3], [0, 1, 2, 3, 4, 3]),
    ([0, 3], [0, 1, 2, 3, 4, 0, 3]),
    ([0, 3, 3, 0], [0, 1, 2, 3, 4, 0, 3, 3, 0]),
])
def test_duplicate_values(indexes, expected):
    lst = [0, 1, 2, 3, 4]

    result = duplicate_values(lst, indexes)

    assert result == expected
