import pandas as pd
from preprocessing.points_features_extractor import PointsFeaturesExtractor
import preprocessing.proportions_calc as proportions


class PointsFeaturesExtractorPriceVolume(PointsFeaturesExtractor):
    def __init__(
            self,
            price_ticks_avg: list[int],
            volume_ticks_avg: list[int]):

        self.price_ticks_avg = price_ticks_avg
        self.price_ticks_calculator = proportions.ProportionsCalc(price_ticks_avg)

        self.volume_ticks_avg = volume_ticks_avg
        self.volume_ticks_calculator = proportions.ProportionsCalc(volume_ticks_avg)

    def get_points_features(self, data_items: pd.DataFrame) -> list[list[float]]:
        close_prices = data_items['close'].astype(float).tolist()
        price_features = self.price_ticks_calculator.calculate(close_prices)

        volume = data_items['volume'].astype(float).tolist()
        volume_features = self.volume_ticks_calculator.calculate(volume)

        return price_features + volume_features

    def get_padding(self) -> tuple[int, int]:
        cut_start = max(self.price_ticks_avg[-1], self.volume_ticks_avg[-1])
        return (cut_start, 0)
