from abc import ABC, abstractmethod

import pandas as pd


class PointsFeaturesExtractor(ABC):

    @abstractmethod
    def get_points_features(self, data_items: pd.DataFrame) -> list[list[float]]:
        pass

    @abstractmethod
    def get_padding(self) -> tuple[int, int]:
        pass
