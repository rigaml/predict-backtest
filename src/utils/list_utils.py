import math
import random
from typing import List, TypeVar
from collections import Counter

T = TypeVar('T')


@staticmethod
def get_indexes_value(lst: List[T], value: T, n: int) -> List[int]:
    '''
    Given a list, get n randomly positions where list contains 'value'
    Parameters:
    - lst: list of 
    - value: value to find in the list
    - n: number of positions to select
    '''
    positions = [i for i, x in enumerate(lst) if x == value]

    if len(positions) < n:
        raise ValueError(f"Found {positions} positions with value: {value} but required {n}")

    selected_positions = random.sample(positions, min(n, len(positions)))

    return selected_positions


@staticmethod
def remove_indexes(lst: List[T], indexes: List[int]) -> List[T]:
    '''
    Given a 'lst' and a list of indexes to remove, return a new list removing the indexes. 
    '''
    result = [lst[i] for i in range(len(lst)) if i not in indexes]
    return result


@staticmethod
def duplicate_values(lst: List[T], indexes: List[int]) -> List[T]:
    '''
    Given a 'lst' and a list of indices to duplicate, 
    return list adding duplicated positions at the end of the list. 
    '''
    result = list(lst)
    for index in indexes:
        result.append(lst[index])

    return result


@staticmethod
def convert_binary(lst: List[T], value_one: T) -> List[int]:
    """
    Given 'lst' generates a new list with 1 if value matches 'value_one' and '0' otherwise.
    """
    result = [1 if x == value_one else 0 for x in lst]
    return result


@staticmethod
def normalize_list(input_list):
    """
    Normalize a list of numbers using Min-Max scaling.

    Parameters:
    - input_list: The input list of numbers.

    Returns:
    - normalized_list: The normalized list.
    """
    min_val = min(input_list)
    max_val = max(input_list)

    normalized_list = [(x - min_val) / (max_val - min_val) for x in input_list]

    return normalized_list


@staticmethod
def display_frequency_classes(classes: List[int], down_pcts: List[float], up_pcts: List[float]):
    # Calculate the frequency of each class
    frequency_dict = Counter(classes)

    num_ticks = len(classes)
    print(f"Total: {num_ticks}")
    for value, frequency in sorted(frequency_dict.items(), key=lambda d: d[0]):
        percent = 0
        if value > 0:
            position = value - len(down_pcts)
            if position < 0:
                percent = -1 * down_pcts[-1 * position - 1]
            elif position > 0:
                percent = up_pcts[position - 1]

        print(f"{(frequency/num_ticks*100):>6.2f}% {frequency:>6} times {percent:>3}% change ({value})")


@staticmethod
def display_frequency_values(values: List[int]):
    # Calculate the frequency of each value
    frequency_dict = Counter(values)

    num_ticks = len(values)
    print(f"Total: {num_ticks}")
    for element, frequency in sorted(frequency_dict.items(), key=lambda d: d[0]):
        print(f"{(frequency/num_ticks*100):>6.2f}% {frequency:>6} times ({element})")


@staticmethod
def calculate_rolling_average(prices: List[float], window: int) -> List[float]:
    rolling_avgs = []
    current_sum = prices[0]
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
def calculate_proportions(prices: List[float], averages_list: List[List[float]]) -> List[List[float]]:
    list_of_list_proportions = []
    for averages in averages_list:
        list_proportions = []
        for idx, average in enumerate(averages):
            list_proportions.append((prices[idx] - average)/prices[idx])

        list_of_list_proportions.append(list_proportions)

    return list_of_list_proportions
