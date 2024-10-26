# abstract class to load data from different sources
from abc import ABC, abstractmethod
import pandas as pd


class BaseRepo(ABC):

    @abstractmethod
    def get_data(self, ticker: str) -> pd.DataFrame:
        pass
