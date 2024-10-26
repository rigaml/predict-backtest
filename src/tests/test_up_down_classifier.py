import unittest
import pytest

from math import nan

# import context
from src.classifiers import up_down_classifier as udc


def test_up_down_classifier_when_window_less_than_2_raises_exception():
    window = 1
    down_pcts = [10, 20]
    up_pcts = [10, 20]

    with pytest.raises(ValueError, match="'window' should be at least 2"):
        udc.UpsDownsClassifier(window, down_pcts, up_pcts)


@pytest.mark.parametrize(
    "down_pcts, up_pcts",
    [([], []),
     ([10], []),
     ([], [10]),
     ],
)
def test_up_down_classifier_when_pcts_length_zero_raises_exception(down_pcts, up_pcts):
    window = 2

    with pytest.raises(ValueError, match=r"'down_pcts' and 'up_pcts' should be at least 1"):
        udc.UpsDownsClassifier(window, down_pcts, up_pcts)


def test_up_down_classifier_when_down_pcts_not_ascending_raises_exception():
    window = 2
    down_pcts = [20, 10]
    up_pcts = [10, 20]

    with pytest.raises(ValueError, match="'down_pcts' and 'up_pcts' values should be in order monotonically ascendingly"):
        udc.UpsDownsClassifier(window, down_pcts, up_pcts)


def test_up_down_classifier_when_up_pcts_not_ascending_raises_exception():
    window = 2
    down_pcts = [10, 20]
    up_pcts = [20, 10]

    with pytest.raises(ValueError, match="'down_pcts' and 'up_pcts' values should be in order monotonically ascendingly"):
        udc.UpsDownsClassifier(window, down_pcts, up_pcts)


def test_up_down_classifier_when_down_pcts_not_greater_than_zero_raises_exception():
    window = 2
    down_pcts = [-10, 20]
    up_pcts = [10, 20]

    with pytest.raises(ValueError, match="'down_pcts' and 'up_pcts' values should greater than 0"):
        udc.UpsDownsClassifier(window, down_pcts, up_pcts)


def test_up_down_classifier_when_up_pcts_not_greater_than_zero_raises_exception():
    window = 2
    down_pcts = [10, 20]
    up_pcts = [-10, 20]

    with pytest.raises(ValueError, match="'down_pcts' and 'up_pcts' values should greater than 0"):
        udc.UpsDownsClassifier(window, down_pcts, up_pcts)


def test_up_down_classifier_classify_when_data_size_is_equal_or_less_than_window_raises_exception():
    window = 2
    down_pcts = [10, 20]
    up_pcts = [10, 20]
    data = [3, 2]

    classifier = udc.UpsDownsClassifier(window, down_pcts, up_pcts)

    with pytest.raises(ValueError, match=r"'data' length should be bigger than 'window'"):
        classifier.classify(data)


def test_up_down_classifier_when_data_values_not_greater_than_zero_raises_exception():
    data = [3, -2, 5]
    window = 2
    down_pcts = [10, 20]
    up_pcts = [10, 20]

    classifier = udc.UpsDownsClassifier(window, down_pcts, up_pcts)

    with pytest.raises(ValueError, match="'data' values should be greater than 0"):
        classifier.classify(data)


def test_up_down_classifier_when_called_valid_parameters_returns_classes_with_minus1s_window():
    data = [3, 2.9, 3.0, 2.8, 2.6]
    window = 2
    down_pcts = [10, 20]
    up_pcts = [10, 20]

    classifier = udc.UpsDownsClassifier(window, down_pcts, up_pcts)
    classes = classifier.classify(data)

    expected = [2, 2, 1, -1, -1]
    assert classes == expected


@pytest.mark.parametrize(
    "data, expected",
    [([1, 1, 1], [2]), ([3, 2.7, 2.8], [2]), ([3, 3.1, 3.2], [2])],
)
def test_find_down_up_classes_when_data_change_small_returns_neutral_class(data, expected):
    window = 2
    down_pcts = [10, 20]
    up_pcts = [10, 20]

    classes = udc.find_down_up_classes(
        data, window, down_pcts, up_pcts
    )

    assert classes == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ([3, 2.6, 3], [1]),
        ([3, 2.9, 2.68], [1]),
        ([3, 2.9, 2.8, 2.5], [2, 1]),
        ([3, 2.9, 3.0, 2.8, 2.6], [2, 2, 1]),
    ],
)
def test_find_down_up_classes_when_1st_down_is_reached_returns_index_1st_down(
    data, expected
):
    window = 2
    down_pcts = [10, 20]
    up_pcts = [10, 20]

    classes = udc.find_down_up_classes(
        data, window, down_pcts, up_pcts
    )

    assert classes == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ([3, 2, 1], [0]),
        ([3, 2.3, 2.6], [0]),
        ([3, 2.6, 2.8, 2.0], [1, 0]),
        ([3, 2.9, 2.8, 2.6, 2.1], [2, 1, 0]),
    ],
)
def test_find_down_up_classes_when_2nd_down_is_reached_returns_index_2nd_down(
    data, expected
):
    window = 2
    down_pcts = [10, 20]
    up_pcts = [10, 20]

    classes = udc.find_down_up_classes(
        data, window, down_pcts, up_pcts
    )

    assert classes == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ([1, 1.1, 1.01], [3]),
        ([1, 1.09, 1.19], [3]),
        ([1, 1.01, 1.09, 1.12], [2, 3]),
        ([1, 1.01, 1.02, 1.1, 1.14], [2, 2, 3]),
    ],
)
def test_find_down_up_classes_when_1st_up_is_reached_returns_index_1st_up(
    data, expected
):
    window = 2
    down_pcts = [10, 20]
    up_pcts = [10, 20]

    classes = udc.find_down_up_classes(
        data, window, down_pcts, up_pcts
    )

    assert classes == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ([1, 1.21, 1.01], [4]),
        ([1, 1.09, 1.21], [4]),
        ([1, 1.01, 1.09, 1.31], [2, 4]),
        ([1, 1.01, 1.09, 1.12, 1.31], [2, 3, 4]),
    ],
)
def test_find_down_up_classes_when_2nd_up_is_reached_returns_index_2nd_up(
    data, expected
):
    window = 2
    down_pcts = [10, 20]
    up_pcts = [10, 20]

    classes = udc.find_down_up_classes(
        data, window, down_pcts, up_pcts
    )

    assert classes == expected


@pytest.mark.parametrize(
    "data, expected",
    [([12, 1, 20], [0]), ([12, 11, 1], [0])],
)
def test_find_down_up_classes_when_down_is_reached_before_up_returns_index_down(
    data, expected
):
    window = 2
    down_pcts = [50, 90]
    up_pcts = [70]

    classes = udc.find_down_up_classes(
        data, window, down_pcts, up_pcts
    )

    assert classes == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ([12, 17, 1.0], [2]),
        ([12, 11, 22], [3]),
        ([12, 5, 17, 16], [2, 3]),
        ([12, 10, 22, 10, 32], [3, 3, 2]),
    ],
)
def test_find_down_up_classes_when_up_is_reached_before_down_returns_index_up(
    data, expected
):
    window = 2
    down_pcts = [60]
    up_pcts = [40, 80]

    classes = udc.find_down_up_classes(
        data, window, down_pcts, up_pcts
    )

    assert classes == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ([10, 11, 12, 13, 180], [13, 20]),
    ],
)
def test_find_down_up_classes_when_many_up_down_pcts_returns_correct_classes(data, expected):
    window = 3
    down_pcts = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    up_pcts = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    classes = udc.find_down_up_classes(
        data, window, down_pcts, up_pcts
    )

    assert classes == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        (
            [
                9.965,
                9.93,
                9.83,
                9.825,
                9.85,
                9.865,
                9.925,
                9.92,
                9.95,
                9.935,
                9.98,
                9.96,
                9.95,
                9.95,
                9.935,
                9.955,
                9.955,
                9.965,
                9.95,
                9.94,
                9.945,
                9.945,
                9.94,
                9.925,
                9.945,
                9.94,
                9.935,
                9.935,
                9.955,
                9.93,
                9.915,
                9.91,
                9.965,
                9.96,
                9.96,
                9.985,
                9.98,
                9.94,
                9.925,
                9.91,
                9.91,
                9.945,
                9.93,
                9.92,
                9.915,
                9.91,
                9.92,
                9.93,
                9.93,
                9.93,
                9.915,
                9.855,
                9.82,
                9.82,
                9.44,
                9.15,
                9.055,
                9.125,
                9.21,
            ],
            [
                1,
                1,
                0,
                0,
                0,
                0,
                0
            ],
        ),
    ],
)
def test_find_down_up_classes_when_long_window_returns_classes_minus_window_length(data, expected):
    window = 52
    down_pcts = [3]
    up_pcts = [7]

    classes = udc.find_down_up_classes(
        data, window, down_pcts, up_pcts
    )

    assert len(data) == len(classes) + window
    assert classes == expected
