import pytest

from src.utils.text_utils import extract_company, extract_days, extract_pcts, is_predict_up


@pytest.mark.parametrize("input_str", [
    ("2024-05-14-2022"),
    ("2024-05-14-2022-20170101-5"),
])
def test_extract_company_when_letters_not_found_in_input_then_raises_exception(input_str):
    with pytest.raises(ValueError):
        extract_company(input_str)


@pytest.mark.parametrize("input_str, expected", [
    ("2024-05-14-2022-U-predictUP-dates20170101", "U"),
    ("2024-05-14-2022-ZM-predictUP-dates20170101", "ZM"),
    ("2024-05-14-2022-TSLA-predictUP-dates20170101", "TSLA"),
    ("2024-05-14-2022-AAPL-", "AAPL"),
    ("2024-05-14-2022-MSFT", "MSFT"),
])
def test_extract_company_when_valid_input_then_correct_company(input_str, expected):
    assert extract_company(input_str) == expected


@pytest.mark.parametrize("input_str", [
    ("2024-05-14-2022-TSLA-day5"),
    ("2024-05-14-2022-TSLA-predictUP-dates20170101-days-down500-600"),
    ("2024-05-14-2022-U-predictUP-dates20170101-daysX")
])
def test_extract_days_when_days_not_found_in_input_then_raises_exception(input_str):
    with pytest.raises(ValueError):
        extract_days(input_str)


@pytest.mark.parametrize("input_str, expected", [
    ("2024-05-14-2022-TSLA-predictUP-dates20170101-days5", 5),
    ("2024-05-14-2022-TSLA-predictUP-dates20170101-days10-down500-600", 10),
    ("2024-05-14-2022-U-predictUP-dates20170101-days200", 200)
])
def test_extract_days_when_valid_input_then_correct_days(input_str, expected):
    assert extract_days(input_str) == expected


@pytest.mark.parametrize("input_str, prefix, expected", [
    ("2024-05-14-2022-TSLA-predictUP-dates20170101-days5-down1-up5", "down", [1.0]),
    ("2024-05-14-2022-TSLA-predictUP-dates20170101-days5-down500-600-up5", "down", [5.0, 6.0]),
    ("2024-05-14-2022-TSLA-predictUP-dates20170101-days5-down500-700-900", "down", [5.0, 7.0, 9.0]),
    ("2024-05-14-2022-TSLA-predictUP-dates20170101-days5-up300-500", "up", [3.0, 5.0])
])
def test_extract_pcts_when_valid_input_then_correct_pcts(input_str, prefix, expected):
    assert extract_pcts(input_str, prefix) == expected


@pytest.mark.parametrize("input_str, prefix", [
    ("2024-05-14-2022-TSLA-predictUP-dates20170101-days5-down500-600-missing5", "up"),
    ("2024-05-14-2022-TSLA-predictUP-dates20170101-days5", "down"),
    ("2024-05-14-2022-TSLA-predictUP-dates20170101-days5", "up")
])
def test_extract_pcts_when_missing_prefix_then_raise_value_error(input_str, prefix):
    with pytest.raises(ValueError):
        extract_pcts(input_str, prefix)


@pytest.mark.parametrize("input_str, expected", [
    ("2024-05-14-2022-TSLA-predictUP-dates20170101", True),
    ("2024-05-14-2022-TSLA-predictDOWN-dates20170101", False),
    ("2024-05-14-2022-TSLA-dates20170101-predictUP-", True),
    ("2024-05-14-2022-TSLA-dates20170101", False)
])
def test_is_predict_up_when_various_inputs_then_correct_boolean(input_str, expected):
    assert is_predict_up(input_str) == expected
