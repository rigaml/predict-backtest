import pytest
from unittest import mock

from typing import List
import pandas as pd
from datetime import datetime, timedelta

from data_sources import tiingo_repo as tr

DAYS_DOWNLOAD = 30


def test_get_data_when_date_start_date_end_same_returns_empty_dataframe():
    client = mock.MagicMock()
    start_date = datetime(2022, 1, 1)
    end_date = start_date
    interval = 15
    after_hours = False
    repo = tr.TiingoRepo(client, start_date, end_date, interval, after_hours)

    result = repo.get_data("AAPL")

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 0


@pytest.mark.parametrize("responses, rows", [
    (["column0,volume,volume\nvalue0,10,10"], 1),
    (["column0,volume\nvalue0,10", None], 1),
    ([None, "column0,volume\nvalue1,10"], 1),
    ([None, "column0,volume\nvalue1,10", None], 1),
    ([None, None, "column0,volume\nvalue2,10", None], 1),
    ([None, None, "column0,volume\nvalue2,10", None, None], 1),
    ([None, "column0,volume\nvalue1,10", "column0,volume\nvalue2,10", None, None], 2),
    (["column0,volume\nvalue0,10", "column0,volume\nvalue1,10", "column0,volume\nvalue2,10", None, None], 3),
    (["column0,volume\nvalue0,10", "column0,volume\nvalue1,10", "column0,volume\nvalue2,10", "column0,volume\nvalue3,10"], 4),
])
def test_get_data_when_responses_without_gaps_returns_responses(responses: List[str | None], rows: int):
    client = mock.MagicMock()
    print(f"responses_with_volume: {responses}")
    client.download_ticker.side_effect = responses

    start_date = datetime(2022, 1, 1)
    end_date = start_date + timedelta(DAYS_DOWNLOAD*len(responses))
    interval = 15
    after_hours = False

    repo = tr.TiingoRepo(client, start_date, end_date, interval, after_hours, 0, DAYS_DOWNLOAD)
    result = repo.get_data("AAPL")

    assert isinstance(result, pd.DataFrame)
    assert result.shape[0] == rows


@pytest.mark.parametrize("responses", [
    (["column0,volume\nvalue0,10", None, "column0,volume\nvalue2,10"]),
    ([None, "column0,volume\nvalue1,10", None, "column0,volume\nvalue3,10"]),
    (["column0,volume\nvalue0,10", "column0,volume\nvalue1,10", None, "column0,volume\nvalue3,10"]),
])
def test_get_data_when_empty_responses_in_the_middle_raises_exception(responses: List[str | None]):
    client = mock.MagicMock()
    client.download_ticker.side_effect = responses

    start_date = datetime(2022, 1, 1)
    end_date = start_date + timedelta(DAYS_DOWNLOAD*len(responses))
    interval = 15
    after_hours = False

    repo = tr.TiingoRepo(client, start_date, end_date, interval, after_hours, 0, DAYS_DOWNLOAD)
    with pytest.raises(tr.DataGapsException):
        repo.get_data("AAPL")
