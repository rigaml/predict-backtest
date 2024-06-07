"""
Loads to memory data for given tickers and date range.
"""
from typing import Callable, Dict, List, Tuple
import pandas as pd

from repositories.base_repo import BaseRepository


class DataTransformer:

    def __init__(self, repo: BaseRepository):
        self.repo = repo
        self.data_source: Dict[str, pd.DataFrame] = {}

    def set_data(self, ticker: str, data: pd.DataFrame) -> None:
        """
        Retrieves the data for some ticker and stores it in the data_source.
        """
        self.data_source[ticker] = data

    def get_features_targets(
        self,
        get_features: Callable[[pd.DataFrame], list],
        get_targets: Callable[[pd.DataFrame], list]
    ) -> Tuple[List[List[float]], List[List[float]]]:
        """
        Applies a function that decides which features to use to each ticker stored data and 
        returns all the features for all the tickers in the data_source and returns a list.

        Args:
            get_features: Function that decides which features to use. Takes a DataFrame as input and returns a list of floats.
            get_targets: Function that decides which targets to use. Takes a DataFrame as input and returns a list of floats.

        Returns:
            A tuple of two lists. The first list contains all the features for all the tickers in the data_source.
            The second list contains all the targets for all the tickers in the data_source.
        """
        features = []
        targets = []
        for _, data in self.data_source.items():
            features.append(get_features(data))
            targets.append(get_targets(data))

        return features, targets
