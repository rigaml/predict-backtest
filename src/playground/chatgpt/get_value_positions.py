## given a list of integers of length M randomly get N positions where it contain value V

import random

def get_indexes_value(lst, value, n):
    # Get indices of elements equal to the specified value
    positions = [i for i, x in enumerate(lst) if x == value]

    # Randomly select N positions
    selected_positions = random.sample(positions, min(n, len(positions)))

    return selected_positions

# Example usage:
my_list = [1, 2, 3, 4, 2, 5, 2, 6, 7, 2]
target_value = 2
num_positions_to_select = 3

result_positions = get_indexes_value(my_list, target_value, num_positions_to_select)
print("Selected positions:", result_positions)
