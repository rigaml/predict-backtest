import numpy as np

from typing import List

from classifiers.base_classifier import BaseClassifier
from utils.validation_utils import are_over_limit


class EwaClassifier(BaseClassifier):
    def __init__(
        self,
        window: int,
        down_pcts: List[float],
        up_pcts: List[float],
        alpha: float,
    ):
        validate_init(window, down_pcts, up_pcts, alpha)

        self.window = window
        self.down_pcts = down_pcts
        self.up_pcts = up_pcts
        self.alpha = alpha

    def classify(self, data) -> List[int]:
        validate_classify(data, self.window)

        classes = find_ewa_classes(
            data, self.window, self.down_pcts, self.up_pcts, self.alpha
        )

        classes.extend([-1] * (len(data) - len(classes)))

        return classes


def validate_init(window: int, down_pcts: float, up_pcts: float, alpha: float):
    """
    Validates input parameters
    """
    if window < 2:
        raise ValueError(f"'window' should be at least 2 (provided: {window})")
    if len(down_pcts) != 1 or len(up_pcts) != 1:
        raise ValueError(
            f"'down_pcts' and 'up_pcts' length should be 1 (provided: {len(down_pcts)} and {len(up_pcts)})"
        )
    if alpha <= 0 or alpha >= 1:
        raise ValueError(
            f"'alpha' should be between 0 and 1 (provided: {alpha})"
        )


def validate_classify(data, window):
    if len(data) <= window:
        raise ValueError(
            f"'data' length should be bigger than 'window' (provided: {len(data)} < window: {window})"
        )
    if (not are_over_limit(data)):
        raise ValueError(
            f"'data' values should be greater than 0"
        )


def find_ewa_classes(
    data: List[float],
    window: int,
    down_pct: float,
    up_pct: float,
    alpha: float,
) -> List[int]:
    classes = [0] * (len(data) - window)
    len_down_pcts = len(down_pct)
    ewas = calculate_ewas(data, alpha)

    for data_idx in range(len(data) - window):
        ewas_window_value = ewas[data_idx + window]
        pct_diff = (ewas_window_value - data[data_idx]) * 100 / data[data_idx]
        if pct_diff <= -1 * down_pct[0]:
            classes[data_idx] = len_down_pcts - 1
        elif pct_diff >= up_pct[0]:
            classes[data_idx] = len_down_pcts + 1
        else:
            classes[data_idx] = len_down_pcts

    return classes


def calculate_ewas(
    data: List[float],
    alpha: float
) -> List[float]:
    """
    Compute the exponentially weighted average sequence (EWAS) of a given data sequence.

    Args:
        data: The input data sequence.
        alpha: The smoothing factor between 0 and 1.

    Returns:
        The EWAS sequence.
    """
    ewas = [0.0] * len(data)
    ewas[0] = data[0]
    for i in range(1, len(data)):
        ewas[i] = (1 - alpha) * ewas[i-1] + alpha * data[i]

    return ewas


def calculate_ewa_alpha(window: int, reach_pct: float) -> float:
    """
    Calculate the alpha value for an Exponential Weighted Average (EWA) based on a specified window size and reach percentage.

    The function determines the smoothing factor (alpha) needed for an EWA calculation, such that a given percentage of the
    weight is concentrated within a specified window of most recent observations. This allows for dynamic adjustment of alpha
    to achieve a desired decay effect over a specified number of periods.

    Parameters:
    - window: Number of periods over which the EWA should significantly weight the observations. This is the span
        across which the reach_pct of the total weight should be distributed.
    - reach_pct: Target percentage (expressed as a decimal) of total weight that should be allocated within the
        specified window. For example, a reach_pct of 0.5 means that 50% of the weight of the EWA calculation should be 
        concentrated within the most recent 'window' periods.

    Returns:
    - The calculated alpha value for the EWA, indicating the degree of weighting decrease for each subsequent observation.
      This value is between 0 and 1, where a higher alpha results in more weight being given to recent observations,
      and a lower alpha spreads the weight more evenly over a longer series of observations.

    Example:
    - To calculate an alpha value such that 50% of the weight is within the last 10 observations, call:
      calculate_ewa_alpha(window=10, reach_pct=0.5)
    """
    return 1 - np.power(1 - reach_pct, 1 / window)
