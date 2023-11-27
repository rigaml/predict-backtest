import math
from typing import List

from modules.validation_utils import is_mono_ascending

class SignalsCalc:
    def __init__(
        self,
        windows: List[int],
    ):
        self.windows = windows

    def calculate(self, data):
        validate_input(data, self.windows)

        windows_rolling_avg = []
        for window in self.windows:
            windows_rolling_avg.append(calculate_rolling_average(data, window))

        return windows_rolling_avg
            

def calculate_rolling_average(data: List[float], window: int):
    rolling_avgs = []
    current_sum= data[0]
    for i in range(1, window):
        current_sum += data[i]
        rolling_avgs.append(math.nan)

    for i in range(window, len(data)):
        rolling_avg = current_sum / window
        rolling_avgs.append(rolling_avg)

        current_sum = current_sum - data[i - window] + data[i]

    # Add rolling average for last element
    rolling_avg = current_sum / window
    rolling_avgs.append(rolling_avg)

    return rolling_avgs


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
