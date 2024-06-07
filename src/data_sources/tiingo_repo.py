# abstract class to load data from different sources
from datetime import datetime, timedelta
import io
import time
import pandas as pd

from apis.tiingo_api import TiingoAPI
from data_sources.base_repo import BaseRepo


class TiingoRepo(BaseRepo):
    """
    Obtains full period data usign the tiingo api.
    """

    def __init__(self, client: TiingoAPI, wait_time: int = 0, days_download: int = 30):
        self.client = client
        self.wait_time = wait_time
        self.days_download = days_download

    def get_data(self, ticker: str, start_date: datetime, end_date: datetime, interval: int, after_hours: bool) -> pd.DataFrame:
        data = []
        data_stopped = False
        current_start_date = start_date
        while current_start_date < end_date:
            current_end_date = min(current_start_date + timedelta(days=self.days_download), end_date)
            response = self.client.download_ticker(
                ticker,
                start_date=current_start_date,
                end_date=current_end_date,
                interval=interval,
                after_hours=after_hours
            )
            if response:
                if data_stopped:
                    raise DataGapsException("Gaps in the data: starts stops and starts again.")

                data.append(pd.read_csv(io.StringIO(response)))
            else:
                if len(data) > 0:
                    data_stopped = True

            current_start_date = current_end_date

            time.sleep(self.wait_time)

        return pd.concat(data) if len(data) > 0 else pd.DataFrame()


class DataGapsException(Exception):
    pass
