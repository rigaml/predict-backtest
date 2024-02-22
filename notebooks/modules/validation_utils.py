@staticmethod
def is_mono_ascending(values) -> bool:
    return all(x < y for x, y in zip(values, values[1:]))


@staticmethod
def are_over(values, low=0) -> bool:
    return all(low < x for x in values)