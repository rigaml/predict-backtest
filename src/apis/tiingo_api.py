from datetime import datetime
import requests

def download_ticker(
    api_key: str,
    ticker: str,
    start_date : datetime,
    end_date : datetime,
    sampling_interval: int,
    after_hours: bool,
):
    url = build_download_url(
        api_key, 
        ticker, 
        start_date, 
        end_date, 
        sampling_interval, 
        after_hours)
    
    print(
        f"Retrieving {ticker} from {start_date} to {end_date} on {sampling_interval}m - {url}"
    )

    return make_request_with_retry(url)

def build_download_url(
    api_key,
    ticker,
    start_date,
    end_date,
    sampling_interval,
    after_hours
):
    """Documentation: https://www.tiingo.com/documentation/iex"""

    start_date_str= start_date.strftime("%Y-%m-%d")
    end_date_str= end_date.strftime("%Y-%m-%d")
    after_hours_str= "true" if after_hours else "false"

    return (
        f"https://api.tiingo.com/iex/{ticker}/prices?"
        f"token={api_key}&"
        f"startDate={start_date_str}&"
        f"endDate={end_date_str}&"
        f"resampleFreq={sampling_interval}min&"
        f"afterHours={after_hours_str}&"
        f"format=csv"
    )

def make_request_with_retry(url, retries=5, delay=1):
    headers = {"Content-Type": "application/json"}
    for attempt in range(retries + 1):
        try:
            response = requests.get(url, headers)
            response.raise_for_status()  # Raise an exception for non-2xx responses
            return response.text
        except requests.RequestException as e:
            if response.status_code == 404:
                print(f"404 error: {e}")
                return None
            if attempt < retries:
                print(f"Transient error occurred. Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                print(f"Error: {e}")
                raise