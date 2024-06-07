# abstract class to load data from different sources
from abc import ABC, abstractmethod
from datetime import datetime
import pandas as pd


class BaseRepo(ABC):

    @abstractmethod
    def get_data(self, ticker: str, start_date: datetime, end_date: datetime, interval: int) -> pd.DataFrame:
        pass
