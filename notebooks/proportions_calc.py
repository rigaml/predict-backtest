import math
from typing import List

from modules.validation_utils import is_mono_ascending

class ProportionsCalc:
    def __init__(
        self,
        windows: List[int],
    ):
        self.windows = windows

    def calculate(self, prices):
        """
        Calculates the averages of the prices for the windows provided and then the proportion from the last price
        """

        validate_input(prices, self.windows)

        windows_rolling_avg = []
        for window in self.windows:
            windows_rolling_avg.append(calculate_rolling_average(prices, window))

        proportions= calculate_proportions(prices, windows_rolling_avg)

        return proportions
            

@staticmethod
def calculate_rolling_average(prices: List[float], window: int) -> List[float]:
    rolling_avgs = []
    current_sum= prices[0]
    for i in range(1, window):
        current_sum += prices[i]
        rolling_avgs.append(math.nan)

    for i in range(window, len(prices)):
        rolling_avg = current_sum / window
        rolling_avgs.append(rolling_avg)

        current_sum = current_sum - prices[i - window] + prices[i]

    # Add rolling average for last element
    rolling_avg = current_sum / window
    rolling_avgs.append(rolling_avg)

    return rolling_avgs

@staticmethod
def calculate_proportions(prices: List[float], averages: List[List[float]]) -> List[List[float]]:
    list_of_list_proportions= []
    for averages in averages:
        list_proportions= []
        for idx in range(len(averages)):
            list_proportions.append((prices[idx]-averages[idx])/prices[idx])

        list_of_list_proportions.append(list_proportions)

    return list_of_list_proportions

def validate_input(data: List[float], windows: List[int]):
    """
    Validates input parameters
    """
    if len(windows) < 1:
        raise ValueError(
            f"Should be provided at least 1 window size"
        )
    if (windows[0] < 2):
        raise ValueError(
            f"Minimun window size is 2 but found {windows[0]}"
        )
    if len(data) <= windows[-1]:
        raise ValueError(
            f"Maximum winodw size {windows[-1]} should be less than data size {len(data)}"
        )
    if not is_mono_ascending(windows):
        raise ValueError(
            f"Window array provided should be in ascending order"
        )
