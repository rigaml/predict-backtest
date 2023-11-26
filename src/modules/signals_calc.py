from typing import List

from modules.validation_utils import are_values_greater, is_mono_ascending

class SignalsCalc:
    def __init__(
        self,
        windows: List[int],
    ):
        self.windows = windows

    def calculate(self, data):
        windows_rolling_avg = []
        for window in range(len(self.windows)):
            windows_rolling_avg.append(calculate_rolling_average(data, window))
            

def calculate_rolling_average(array, window):
    rolling_avgs = []
    current_sum = sum(array[:window])

    for i in range(window, len(array)):
        rolling_avg = current_sum / window
        rolling_avgs.append(rolling_avg)

        current_sum = current_sum - array[i - window] + array[i]

    # Add rolling average for last element
    rolling_avg = current_sum / window
    rolling_avgs.append(rolling_avg)

    return rolling_avgs


def validate_input(data, windows):
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
    if len(data) <= windows[:-1]:
        raise ValueError(
            f"Maximum winodw size {windows[:-1]} should be less than data size {len(data)}"
        )
    if not is_mono_ascending(windows):
        raise ValueError(
            f"Window array provided should be in ascending order"
        )
