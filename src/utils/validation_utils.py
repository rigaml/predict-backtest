from typing import List, Union


@staticmethod
def is_mono_ascending(lst: List[Union[int, float]]) -> bool:
    return all(x < y for x, y in zip(lst, lst[1:]))


@staticmethod
def are_over_limit(lst: List[Union[int, float]], lower_limit=0) -> bool:
    return all(lower_limit < x for x in lst)