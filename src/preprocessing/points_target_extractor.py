import pandas as pd
import classifiers.up_down_classifier as udc
import classifiers.ewa_classifier as ec


class PointsTargetExtractor:
    def __init__(
            self,
            ticks_predict: int,
            reach_pct: float,
            down_pcts_predict: list[float],
            up_pcts_predict: list[float]):

        self.ticks_predict = ticks_predict

        self.alpha = ec.calculate_ewa_alpha(self.ticks_predict, reach_pct)
        self.up_downs_classifier = udc.UpsDownsClassifier(self.ticks_predict, down_pcts_predict, up_pcts_predict)

    def get_points_target(self, data_items: pd.DataFrame) -> list[int]:

        close_prices = [float(price) for price in data_items['close']]
        close_price_ewas = ec.calculate_ewas(close_prices, self.alpha)

        return self.up_downs_classifier.classify(close_price_ewas)

    def get_padding(self) -> tuple[int, int]:
        return (0, self.ticks_predict)
