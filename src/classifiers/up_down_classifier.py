from typing import List

from classifiers.base_classifier import BaseClassifier
from utils.validation_utils import are_over_limit, is_mono_ascending


class UpsDownsClassifier(BaseClassifier):
    def __init__(
        self,
        window: int,
        down_pcts: List[float],
        up_pcts: List[float],
        trace_print=False
    ):
        validate_init(window, down_pcts, up_pcts)

        self.window = window
        self.down_pcts = down_pcts
        self.up_pcts = up_pcts
        self.trace_print = trace_print

    def classify(self, data) -> List[int]:
        validate_classify(data, self.window)

        classes = find_down_up_classes(
            data, self.window, self.down_pcts, self.up_pcts, self.trace_print
        )

        classes.extend([-1] * (len(data) - len(classes)))

        return classes


def validate_init(window, down_pcts, up_pcts):
    """
    Validates input parameters
    """
    if window < 2:
        raise ValueError(f"'window' should be at least 2 (provided: {window})")
    if len(down_pcts) < 1 or len(up_pcts) < 1:
        raise ValueError(
            "'down_pcts' and 'up_pcts' should be at least 1 "
            f"(provided:{len(down_pcts)} and {len(up_pcts)} respectively)"
        )
    if not is_mono_ascending(down_pcts) or not is_mono_ascending(up_pcts):
        raise ValueError(
            f"'down_pcts' and 'up_pcts' values should be in order monotonically ascendingly"
        )
    if (not are_over_limit(down_pcts) or not are_over_limit(up_pcts)):
        raise ValueError(
            f"'down_pcts' and 'up_pcts' values should greater than 0"
        )


def validate_classify(data, window):
    if len(data) <= window:
        raise ValueError(
            f"'data' length should be bigger than 'window' (data: {len(data)} <= window: {window})"
        )
    if (not are_over_limit(data)):
        raise ValueError(
            f"'data' values should be greater than 0"
        )


def find_down_up_classes(
    data: List[float],
    window: int,
    down_pcts: List[float],
    up_pcts: List[float],
    trace_print=False,
) -> List[int]:
    classes = [0] * (len(data) - window)

    if trace_print:
        print(f"\ndata={data}")
        print(f"out loop from 0 to {len(data) - window - 1}")

    for data_idx in range(len(data) - window):
        item_class = find_down_up_class_window(data, window, down_pcts, up_pcts, data_idx, trace_print)
        classes[data_idx] = item_class

    return classes


def find_down_up_class_window(
    data: List[float],
    window: int,
    down_pcts: List[float],
    up_pcts: List[float],
    data_idx: int,
    trace_print: bool,
):
    """
    Finds first down_pcts/up_pcts reached in the data window period after each data point.
    If arrives to multiple up_pcts values (without any down_pcts) the class returned should be the maximum up_pcts achieved. (same with down_pcts)
    If arrives to a down_pcts and up_pcts in the window period (or the other way around) the class returned should be the first achieved in the period.
    If no value of down_pcts nor up_pcts is reached, returns len(down_pcts) value.

    Args:
        data: values were to calculate the down or up
        window: number of items after the data item where the down_pcts or up_pcts is going to be searched.
        up_pcts: percentage from a data item point to reach. Values ascending order.
        down_pcts: percentage from a data item point to reach (positive value). Values ascending order.
    Returns:
        Index indicating the up_pcts or down_pcts threshold reached in the window period after each data point.
        Index starts at 0, corresponding to len(down_pcts)-1 value and ends at len(down_pcts) + len(up_pcts) - 1
    """
    # Set the value class id of a class that is to do nothing
    neutral_class_index = len(down_pcts)
    item_class = neutral_class_index

    inital_value = data[data_idx]

    down_pct_idx_max = 0
    down_pct_found = False
    up_pct_idx_max = 0
    up_pct_found = False

    if trace_print:
        print(f"in loop from {data_idx + 1} to {data_idx + 1 + window - 1}")
    for window_idx in range(data_idx + 1, data_idx + 1 + window):
        pct_diff = (data[window_idx] - inital_value) * 100 / inital_value
        if trace_print:
            print(
                f"window initial={inital_value} "
                f"value={data[window_idx]} window_idx={window_idx} pct_down={pct_diff:.2f}"
            )
        for pct_idx in range(down_pct_idx_max, len(down_pcts)):
            if trace_print:
                print(f"down_pcts idx: {pct_idx} {down_pcts[pct_idx]}")
            if pct_diff * -1 >= down_pcts[pct_idx]:
                if up_pct_found:
                    return item_class

                down_pct_found = True
                down_pct_idx_max = pct_idx
                item_class = neutral_class_index - pct_idx - 1

        for pct_idx in range(up_pct_idx_max, len(up_pcts)):
            if trace_print:
                print(f"up_pcts idx: {pct_idx} {up_pcts[pct_idx]}")
            if pct_diff >= up_pcts[pct_idx]:
                if down_pct_found:
                    return item_class

                up_pct_found = True
                up_pct_idx_max = pct_idx
                item_class = neutral_class_index + pct_idx + 1

        if down_pct_found and down_pct_idx_max == len(down_pcts) - 1:
            return item_class

        if up_pct_found and up_pct_idx_max == len(up_pcts) - 1:
            return item_class

    return item_class
