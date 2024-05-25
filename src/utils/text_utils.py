
import re
from typing import List


def extract_company(input_str: str) -> str:
    """Extract the name of the company from the input_str"""
    start_idx = next((i for i, c in enumerate(input_str) if c.isalpha()), None)
    if start_idx is None:
        raise ValueError("Didn't find company name")

    end_idx = input_str.find("-", start_idx)
    if end_idx == -1:
        end_idx = len(input_str)

    return input_str[start_idx:end_idx]


def extract_days(input_str: str) -> int:
    prefix = "-days"
    start_idx = input_str.find(prefix)
    if start_idx == -1:
        raise ValueError(f"Didn't find {prefix}")

    end_idx = input_str.find("-", start_idx+len(prefix))
    if end_idx == -1:
        end_idx = len(input_str)

    return int(input_str[start_idx+len(prefix):end_idx])


def extract_pcts(input_str: str, prefix: str) -> List[float]:
    expression = "-" + prefix + r"(\d+(?:-\d+)*)"
    down_match = re.search(expression, input_str)

    if down_match:
        down_numbers_str = down_match.group(1)

        return [float(num) / 100 if len(num) == 3 else float(num) for num in down_numbers_str.split('-')]

    raise ValueError(f"Didn't find expression '{expression}'")


def is_predict_up(input_str: str):
    return "-predictUP-" in input_str


def shorten_date(input_str: str):
    return input_str[:10].replace("-", "")
