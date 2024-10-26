import pandas as pd
from preprocessing.points_features_extractor import PointsFeaturesExtractor
import preprocessing.proportions_calc as proportions
from utils.date_time_utils import time_fraction_of_day


class PointsFeaturesExtractorPriceTime(PointsFeaturesExtractor):
    def __init__(
            self,
            price_ticks_avg: list[int]):

        self.price_ticks_avg = price_ticks_avg
        self.proportions_calculator = proportions.ProportionsCalc(price_ticks_avg)

    def get_points_features(self, data_items: pd.DataFrame) -> list[list[float]]:
        close_prices = data_items['close'].astype(float).tolist()
        features = self.proportions_calculator.calculate(close_prices)

        dates = data_items['date'].tolist()
        time_fraction = [time_fraction_of_day(date) for date in dates]

        features.append(time_fraction)

        return features

    def get_padding(self) -> tuple[int, int]:
        return (self.price_ticks_avg[-1], 0)
