import pytest
from datetime import datetime
from unittest.mock import patch
from src.utils.date_time_utils import time_fraction_of_day


@pytest.mark.parametrize("datetime_str, fraction_time", [
    ('2022-01-01T00:00:00', 0.0),
    ('2022-01-01T10:30:00', 0.4375),
    ('2022-01-01T12:00:00', 0.5),
    ('2022-01-01T23:59:59', 0.999988425925926),
])
def test_time_fraction_of_day(datetime_str: str, fraction_time: float):
    result = time_fraction_of_day(datetime_str)
    assert result == fraction_time
