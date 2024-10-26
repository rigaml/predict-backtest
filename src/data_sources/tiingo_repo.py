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

    def __init__(
            self,
            client: TiingoAPI,
            start_date: datetime,
            end_date: datetime,
            interval: int = 15,
            after_hours: bool = False,
            wait_time: int = 1,
            days_download: int = 365):
        """
        Args:
            client (TiingoAPI): The client to use to download data.
            wait_time (int, optional): Wait between requests to avoid overwhelm the server and get access denised. Defaults to 0.
            days_download (int, optional): Retrieve data in chunks as there is a limit on how much data can be downloaded in one request. Defaults to 30.
        """
        self.client = client
        self.start_date = start_date
        self.end_date = end_date
        self.interval = interval
        self.after_hours = after_hours
        self.wait_time = wait_time
        self.days_download = days_download

    def get_data(self, ticker: str) -> pd.DataFrame:
        """
        Obtains full period data usign the tiingo api. 
        Retrieval is divided in days as Tiingo has a limit on how much data can be downloaded in one request.
        """
        data = []
        data_stopped = False
        current_start_date = self.start_date
        while current_start_date < self.end_date:
            current_end_date = min(current_start_date + timedelta(days=self.days_download), self.end_date)
            print(f"{ticker} current_start_date: {current_start_date} current_end_date: {current_end_date}")
            response = self.client.download_ticker(
                ticker,
                start_date=current_start_date,
                end_date=current_end_date,
                interval=self.interval,
                after_hours=self.after_hours
            )
            if response:
                if data_stopped:
                    raise DataGapsException("Gaps in the data: starts stops and starts again.")

                interval_data = pd.read_csv(io.StringIO(response))
                if interval_data.shape[0] > 0:
                    print(f"Rows returned: {interval_data.shape[0]}")
                    data.append(interval_data)
                else:
                    print(f"No data returned for {ticker} current_start_date: {
                          current_start_date} current_end_date: {current_end_date}")
            else:
                if len(data) > 0:
                    data_stopped = True

            current_start_date = current_end_date + timedelta(days=1)

            time.sleep(self.wait_time)

        if len(data) == 0:
            return pd.DataFrame()

        full_data = pd.concat(data, axis=0, ignore_index=True)
        print(f"Rows full data: {full_data.shape[0]}")
        # Removing data for public holidays. On these days data is returned with volume is 0 and all values of the day are the same:
        # 2023-01-02 09:30:00-05:00	123.22	123.22	123.22	123.22	0.0
        # 2023-01-02 09:45:00-05:00	123.22	123.22	123.22	123.22	0.0
        full_data.drop(full_data[full_data['volume'] == 0].index, inplace=True)
        print(f"Rows after clean: {full_data.shape[0]}")

        return full_data


class DataGapsException(Exception):
    pass
