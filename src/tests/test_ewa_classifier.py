import unittest
import pytest

from math import nan, isclose

import context
from classifiers import ewa_classifier as ec


def test_ewa_classifier_when_window_less_than_2_raises_exception():
    window = 1
    down_pcts = [10.]
    up_pcts = [10.]
    alpha = 0.5

    with pytest.raises(ValueError, match="'window' should be at least 2"):
        ec.EwaClassifier(window, down_pcts, up_pcts, alpha)


@pytest.mark.parametrize(
    "down_pcts, up_pcts",
    [([], []),
     ([10.], []),
     ([], [10.]),
     ([10., 15.], [10.]),
     ([10.], [10., 15.]),
     ])
def test_ewa_classifier_when_pcts_length_not_1_raises_exception(down_pcts, up_pcts):
    window = 2
    alpha = 0.5

    with pytest.raises(ValueError, match=r"'down_pcts' and 'up_pcts' length should be 1"):
        ec.EwaClassifier(window, down_pcts, up_pcts, alpha)


@pytest.mark.parametrize(
    "alpha",
    [(0),
     (1),
     (-5),
     (5),
     ])
def test_ewa_classifier_when_alpha_not_between_zero_and_one_raises_exception(alpha):
    window = 1
    down_pcts = [10.]
    up_pcts = [10.]

    with pytest.raises(ValueError, match="'window' should be at least 2"):
        ec.EwaClassifier(window, down_pcts, up_pcts, alpha)


def test_ewa_classifier_classify_when_data_size_is_equal_or_less_than_window_raises_exception():
    data = [3, 2]
    window = 2
    down_pcts = [10.]
    up_pcts = [10.]
    alpha = 0.5

    classifier = ec.EwaClassifier(window, down_pcts, up_pcts, alpha)

    with pytest.raises(ValueError, match=r"'data' length should be bigger than 'window'"):
        classifier.classify(data)


def test_ewa_classifier_when_data_values_not_greater_than_zero_raises_exception():
    data = [3, -2, 5]
    window = 2
    down_pcts = [10.]
    up_pcts = [10.]
    alpha = 0.5

    classifier = ec.EwaClassifier(window, down_pcts, up_pcts, alpha)

    with pytest.raises(ValueError, match="'data' values should be greater than 0"):
        classifier.classify(data)


def test_ewa_classifier_when_valid_parameters_returns_classes_with_minus1s_window():
    data = [5.2, 4.9, 5.5, 4.9, 5.2]
    window = 2
    down_pcts = [5.]
    up_pcts = [10.]
    alpha = 0.5

    classifier = ec.EwaClassifier(window, down_pcts, up_pcts, alpha)
    classes = classifier.classify(data)

    expected = [1, 1, 0, -1, -1]
    assert classes == expected


def test_find_ewa_classes_when_empty_data_raises_exception():
    data = []
    window = 2
    down_pcts = [1.0]
    up_pcts = [1.0]
    alpha = 0.5

    with pytest.raises(IndexError):
        ec.find_ewa_classes(data, window, down_pcts, up_pcts, alpha)


@pytest.mark.parametrize(
    "data, window, down_pcts, up_pcts, expected", [
        ([5, 4, 5, 4, 4], 0, [1.0], [5.0], [1, 2, 0, 2, 1]),
        ([5.2, 4.9, 5.5, 4.9, 5.2, 5.7, 5.4, 5.8, 5.9, 6, 5.2, 4.8], 2, [5.0], [10.0], [1, 1, 0, 2, 1, 1, 1, 1, 0, 0])
    ])
def test_find_ewa_classes_when_correct_parameters_then_gets_correct_classes(data, window, down_pcts, up_pcts, expected):
    alpha = 0.5

    ewas_classes = ec.find_ewa_classes(data, window, down_pcts, up_pcts, alpha)

    assert len(ewas_classes) == len(expected)
    assert all(ewa_class == expect_ewa for ewa_class, expect_ewa in zip(ewas_classes, expected))


def test_calculate_ewas_when_empty_data_raises_exception():
    data = []
    alpha = 0.23
    with pytest.raises(IndexError):
        ec.calculate_ewas(data, alpha)


def test_calculate_ewas_when_single_value_returns_value():
    data = [1.0]
    alpha = 0.23
    assert ec.calculate_ewas(data, alpha) == [1.0]


def test_calculate_ewas_when_constant_values_returns_values():
    data = [2.0, 2.0, 2.0, 2.0, 2.0]
    alpha = 0.1
    assert all(isclose(ewa, 2.0) for ewa in ec.calculate_ewas(data, alpha))


def test_calculate_ewas_when_increasing_values_returns_increasing_values():
    data = [1.0, 2.0, 3.0, 4.0, 5.0]
    alpha = 0.23
    ewas = ec.calculate_ewas(data, alpha)
    assert len(ewas) == len(data)
    assert all(ewas[i] <= ewas[i+1] for i in range(len(ewas)-1))


def test_calculate_ewas_when_decreasing_values_returns_decreasing_values():
    data = [5.0, 4.0, 3.0, 2.0, 1.0]
    alpha = 0.23
    ewas = ec.calculate_ewas(data, alpha)
    assert len(ewas) == len(data)
    assert all(ewas[i] >= ewas[i+1] for i in range(len(ewas)-1))


def test_calculate_ewas_when_valid_parameters_returns_correct_ewas():
    data = [5.2, 4.9, 5.5, 4.9, 5.2, 5.7, 5.4, 5.8, 5.9, 6, 5.2, 4.8]
    expected = [5.2, 5.05, 5.275, 5.0875, 5.1438, 5.4219, 5.4109, 5.6055, 5.7527, 5.8764, 5.5382, 5.1691]
    alpha = 0.5

    ewas_result = ec.calculate_ewas(data, alpha)

    assert all(isclose(ewa, exp, abs_tol=0.0001) for ewa, exp in zip(ewas_result, expected))


def test_calculate_ewa_alpha_when_window_and_pct_then_sum_window_for_alpha_achieves_pct():
    n = 2000
    window = 50
    required_pct = 0.95
    alpha = ec.calculate_ewa_alpha(window, required_pct)

    ewas_alpha = [alpha*(1-alpha)**r for r in range(n)]
    print(f"\nalpha: {alpha}")
    sum_first = sum(ewas_alpha[:window])
    sum_last = sum(ewas_alpha[window+1:])
    obtained_pct = sum_first / (sum_first+sum_last)
    print(f"Sum first: {sum_first}\nSum Last: {sum_last}\nObtained%: {obtained_pct}\nRequired%: {required_pct}")
    assert isclose(obtained_pct, required_pct, abs_tol=0.01)
