from typing import List
import pytest
from unittest import mock
import pandas as pd
from datetime import datetime, timedelta

import tests.context
from data_sources import tiingo_repo as tr


def test_get_data_when_date_start_date_end_same_returns_empty_dataframe():
    client = mock.MagicMock()
    repo = tr.TiingoRepo(client)
    start_date = datetime(2022, 1, 1)
    end_date = start_date
    interval = 15
    after_hours = False

    result = repo.get_data("AAPL", start_date, end_date, interval, after_hours)

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 0


@pytest.mark.parametrize("responses, rows", [
    (["column0\nvalue0"], 1),
    (["column0\nvalue0", None], 1),
    ([None, "column0\nvalue1"], 1),
    ([None, "column0\nvalue1", None], 1),
    ([None, None, "column0\nvalue2", None], 1),
    ([None, None, "column0\nvalue2", None, None], 1),
    ([None, "column0\nvalue1", "column0\nvalue2", None, None], 2),
    (["column0\nvalue0", "column0\nvalue1", "column0\nvalue2", None, None], 3),
    (["column0\nvalue0", "column0\nvalue1", "column0\nvalue2", "column0\nvalue3"], 4),
])
def test_get_data_when_responses_without_gaps_returns_responses(responses: List[str | None], rows: int):
    client = mock.MagicMock()
    client.download_ticker.side_effect = responses

    start_date = datetime(2022, 1, 1)
    end_date = start_date + timedelta(30*len(responses))
    interval = 15
    after_hours = False

    repo = tr.TiingoRepo(client)
    result = repo.get_data("AAPL", start_date, end_date, interval, after_hours)

    assert isinstance(result, pd.DataFrame)
    assert result.shape[0] == rows


@pytest.mark.parametrize("responses", [
    (["column0\nvalue0", None, "column0\nvalue2"]),
    ([None, "column0\nvalue1", None, "column0\nvalue3"]),
    (["column0\nvalue0", "column0\nvalue1", None, "column0\nvalue3"]),
])
def test_get_data_when_empty_responses_in_the_middle_raises_exception(responses: List[str | None]):
    client = mock.MagicMock()
    client.download_ticker.side_effect = responses

    start_date = datetime(2022, 1, 1)
    end_date = start_date + timedelta(30*len(responses))
    interval = 15
    after_hours = False

    repo = tr.TiingoRepo(client)
    with pytest.raises(tr.DataGapsException):
        repo.get_data("AAPL", start_date, end_date, interval, after_hours)
