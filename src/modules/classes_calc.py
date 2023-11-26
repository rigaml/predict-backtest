from typing import List

class ClassesCalc:
    def __init__(
        self,
        window: int,
        down_pcts: List[float],
        up_pcts: List[float],
    ):
        self.window = window
        self.down_pcts = down_pcts
        self.up_pcts = up_pcts

    def calculate(self, data):
        classes = find_first_up_down(
            data, self.window, self.down_pcts, self.up_pcts
        )
        # TODO fill the end where classes can not be found with values?
        return classes

def find_first_up_down(
    data: List[float],
    window: int,
    down_pcts: List[float],
    up_pcts: List[float],
) -> List[int]:
    """
    Calculates the maximum threshold reached in the window period after each data point
    If arrives to many positive threshold (without negatives) the class returned should be the maximum threshold achieved.
    If arrives to positive and negative threshold (or the other way around ) the class returned should be the first achieved. Later inspections in time should give the other value direction.

    Args:
        data: prices in ascending date order.
        window: number of items after the data item where the down_pcts or up_pcts is going to be tested.
        down_pcts: percentage from a data item point to reach (positive value).
        up_pcts: percentage from a data item point to reach.
    Returns:
      Array with the maximum threshold reached in the window period after each data point
    """
    validate_input(data, window, down_pcts, up_pcts)

    classes = []

    print(f"\ndata={data}")
    print(f"out loop from 0 to {len(data) - window - 1}")
    for data_idx in range(len(data) - window):
        item_class = find_window_class(data, window, down_pcts, up_pcts, data_idx)

        classes.append(item_class)

    return classes


def find_window_class(
    data: List[float],
    window: int,
    down_pcts: List[float],
    up_pcts: List[float],
    data_idx: int,
):
    # Set the value class id of a class that is to do nothing
    neutral_class = len(down_pcts)
    item_class = neutral_class

    inital_value = data[data_idx]

    down_pct_idx_max = 0
    down_pct_found = False
    up_pct_idx_max = 0
    up_pct_found = False

    print(f"in loop from {data_idx + 1} to {data_idx + 1 + window - 1}")
    for window_idx in range(data_idx + 1, data_idx + 1 + window):
        pct_diff = (inital_value - data[window_idx]) * 100 / inital_value
        print(
            f"window initial={inital_value} value={data[window_idx]} window_idx={window_idx} pct_down={pct_diff:.2f}"
        )        
        for pct_idx in range(down_pct_idx_max, len(down_pcts)):
            print(f"down_pcts idx: {pct_idx} {down_pcts[pct_idx]}")
            if pct_diff >= down_pcts[pct_idx]:
                if up_pct_found:
                    return item_class

                down_pct_found = True
                down_pct_idx_max = pct_idx
                item_class = neutral_class - pct_idx - 1

        for pct_idx in range(up_pct_idx_max, len(up_pcts)):
            print(f"up_pcts idx: {pct_idx} {up_pcts[pct_idx]}")
            if pct_diff * -1 >= up_pcts[pct_idx]:
                if down_pct_found:
                    return item_class

                up_pct_found = True
                up_pct_idx_max = pct_idx
                item_class = neutral_class + pct_idx + 1

        if down_pct_found and down_pct_idx_max == len(down_pcts) - 1:
            return item_class

        if up_pct_found and up_pct_idx_max == len(up_pcts) - 1:
            return item_class

    return item_class


def validate_input(data, window, down_pcts, up_pcts):
    """
    Validates input parameters
    """
    if window < 2:
        raise ValueError(f"'window' should be at least 2 to but {window}")
    if len(down_pcts) < 1 or len(up_pcts) < 1:
        raise ValueError(
            f"'down_pcts' and 'up_pcts' should be at least 1 but are {len(down_pcts)} and {len(up_pcts)} respectively"
        )
    if len(data) <= window:
        raise ValueError(
            f"'data' length should bigger than 'window' but data: {len(data)} < window: {window}"
        )
    if not is_mono_ascending(down_pcts) or not is_mono_ascending(up_pcts):
        raise ValueError(
            f"'down_pcts' and 'up_pcts' values should be in order monotonically ascendingly"
        )
    if (
        not are_values_greater(down_pcts)
        or not are_values_greater(up_pcts)
        or not are_values_greater(data)
    ):
        raise ValueError(
            f"'down_pcts' and 'up_pcts' and 'data' values should greater than 0"
        )


def is_mono_ascending(lst) -> bool:
    return all(x < y for x, y in zip(lst, lst[1:]))


def are_values_greater(lst, lower_bound=0) -> bool:
    return all(lower_bound < x for x in lst)
