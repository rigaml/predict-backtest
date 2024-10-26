import pandas as pd
from preprocessing.points_features_extractor import PointsFeaturesExtractor
import preprocessing.proportions_calc as proportions


class PointsFeaturesExtractorPrice(PointsFeaturesExtractor):
    def __init__(
            self,
            days_averages: list[int]):

        self.days_averages = days_averages
        self.proportions_calculator = proportions.ProportionsCalc(days_averages)

    def get_points_features(self, data_items: pd.DataFrame) -> list[list[float]]:

        close_prices = data_items['close'].astype(float).tolist()
        return self.proportions_calculator.calculate(close_prices)

    def get_padding(self) -> tuple[int, int]:
        return (self.days_averages[-1] - 1, 0)
