@staticmethod
def is_mono_ascending(lst) -> bool:
    return all(x < y for x, y in zip(lst, lst[1:]))


@staticmethod
def are_values_greater(lst, lower_bound=0) -> bool:
    return all(lower_bound < x for x in lst)