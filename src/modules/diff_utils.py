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