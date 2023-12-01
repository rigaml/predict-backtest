import random
from typing import List

@staticmethod
def calculate_price_proportions(prices: List[float], averages_list: List[List[float]]) -> List[List[float]]:
    list_of_list_proportions= []
    for averages in averages_list:
        list_proportions= []
        for idx in range(len(averages)):
            list_proportions.append((prices[idx]-averages[idx])/prices[idx])

        list_of_list_proportions.append(list_proportions)

    return list_of_list_proportions

@staticmethod
def get_indexes_value(lst: List[int], value: int, n: int) -> List[int]:
    '''
    Given a list of integers of length M randomly get N positions where it contain value V
    '''
    positions = [i for i, x in enumerate(lst) if x == value]

    # Randomly select N positions
    selected_positions = random.sample(positions, min(n, len(positions)))

    return selected_positions


def remove_indexes(lst: List[int], indexes: List[int]) -> List[int]:
    '''
    Given a list of integers 'r' that are indexes on list 'a' create a new list 'b' removing from 'a' the indexes in 'r' 
    '''
    # Create a new list 'b' without the elements at the specified indices
    result = [lst[i] for i in range(len(lst)) if i not in indexes]
    return result

@staticmethod
def convert_binary(lst: List[int], value_one: int) -> List[int]:
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