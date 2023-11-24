from typing import List
import pandas as pd

# Numbers in ascending order (Fibonacci numbers)
INTERVALS = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584]

class InputsGenerator:

    def __init__(self, intervals: List[int]) -> None:
        self.intervals = intervals

    def add_mean_differences(self, data: pd.DataFrame, columns: List[str]):
        bigger_interval= self.intervals[-1]
        result = {}

        for idx, value in data[column].iloc[bigger_interval:]:                
            for column in columns:
                for interval in self.intervals:
                    interval_diffs = []
                    inteval_diff= sum(data[column], idx - interval, idx) / interval
                    interval_diffs.append(inteval_diff)

                result.update({column + str(interval) :  interval_diffs})
