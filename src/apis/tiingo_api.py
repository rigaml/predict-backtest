from datetime import datetime
from http import client
import time
from typing import Optional
import requests
import logging

logger = logging.getLogger(__name__)


class TiingoAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    def download_ticker(
        self,
        ticker: str,
        start_date: datetime,
        end_date: datetime,
        interval: int,
        after_hours: bool,
    ) -> Optional[str]:
        """Retrieve ticker data from Tiingo API.

        Args:
            ticker (str): The ticker symbol.
            start_date (datetime): The start date of the data.
            end_date (datetime): The end date of the data.
            interval (int): The interval in minutes between data points.
            after_hours (bool): Whether to include after-hours data.

        Returns:
            str: The CSV data response from the API.
        """
        url = self.build_download_url(
            ticker,
            start_date,
            end_date,
            interval,
            after_hours
        )

        logger.debug(
            f"Retrieving {ticker} from {start_date} to {end_date} on {interval}m - {url}"
        )

        return self.request_url_with_retry(url)

    def build_download_url(
        self,
        ticker,
        start_date,
        end_date,
        sampling_interval,
        after_hours
    ) -> str:
        """Documentation: https://www.tiingo.com/documentation/iex"""

        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")
        after_hours_str = "true" if after_hours else "false"

        return (
            f"https://api.tiingo.com/iex/{ticker}/prices?"
            f"token={self.api_key}&"
            f"startDate={start_date_str}&"
            f"endDate={end_date_str}&"
            f"resampleFreq={sampling_interval}min&"
            f"afterHours={after_hours_str}&"
            f"format=csv"
        )

    def request_url_with_retry(self, url: str, params=None, retries: int = 5, delay: int = 1) -> Optional[str]:
        headers = {"Content-Type": "application/json"}

        for attempt in range(1, retries + 1):
            try:
                response = requests.get(url, params=params, headers=headers)
                response.raise_for_status()
                return response.text
            # Use `HTTPError` for Http errors (status codes 404, 403...)
            except requests.exceptions.HTTPError as http_err:
                if http_err.response.status_code == client.NOT_FOUND:
                    logger.warning(f"Requesting {url} got 404 NOT FOUND", http_err)
                    return None
                else:
                    # Since not transient error, should exit
                    logger.error(f"Requested {url} got http error.", http_err)
                    raise Exception(f"Requested {url} got http error.", http_err)
            # Use `RequestException` for network related issues like connection errors, timeouts
            except requests.exceptions.RequestException as req_err:
                if attempt < retries:
                    logger.info(
                        f"Requested {url} got network error. Retrying in {delay} seconds...", req_err)
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff
                else:
                    logger.error(
                        f"Retried {url} for {attempt} times got network errors. Aborting!", req_err)
                    raise Exception(f"Retried {url} for {attempt} times got network errors. Aborting!", req_err)
