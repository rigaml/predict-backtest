import pandas as pd
from data_sources.base_repo import BaseRepo


class DataLoader:
    def __init__(self, repo: BaseRepo):
        self.repo = repo

    def load_data(self, data_ids: list[str]) -> list[pd.DataFrame]:
        data = []
        for id in data_ids:
            data.append(self.repo.get_data(id))

        return data
