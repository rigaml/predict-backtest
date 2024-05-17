from typing import List

from utils.validation_utils import is_mono_ascending
from utils.list_utils import calculate_proportions, calculate_rolling_average

class ProportionsCalc:
    def __init__(
        self,
        windows: List[int],
    ):
        self.windows = windows

    def calculate(self, prices) -> List[List[float]]:
        """
        Calculates the averages of the prices for the windows provided and then the proportion from the last price
        """
        validate_input(prices, self.windows)

        windows_rolling_avg = []
        for window in self.windows:
            windows_rolling_avg.append(calculate_rolling_average(prices, window))

        proportions = calculate_proportions(prices, windows_rolling_avg)

        return proportions

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
