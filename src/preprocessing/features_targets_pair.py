
"""
Loads to memory data for given tickers and date range.
"""
import pandas as pd

from preprocessing.points_features_extractor import PointsFeaturesExtractor
from preprocessing.points_target_extractor import PointsTargetExtractor
from utils.list_utils import safe_slice


class FeaturesTargetsPair:

    def __init__(
        self,
        features_extractor: PointsFeaturesExtractor,
        targets_extractor: PointsTargetExtractor
    ):
        self.features_extractor = features_extractor
        self.targets_extractor = targets_extractor

    def align(
        self,
        data_items: list[pd.DataFrame]
    ) -> tuple[list[list[float]], list[int]]:
        """
        Applies a function that extracts features and targets to use to each data_item 
        returns all the features for all the tickers in the data_source and returns a list.

        Args:
            get_features: gets features to use. Takes a DataFrame as input and returns a list of floats.
            get_targets: gets targets to use. Takes a DataFrame as input and returns a list of floats.

        Returns:
            A tuple of two lists. The first list contains all the features for all the tickers in the data_source.
            The second list contains all the targets for all the tickers in the data_source.
        """
        features_padding = self.features_extractor.get_padding()
        targets_padding = self.targets_extractor.get_padding()
        start_padding = max(features_padding[0], targets_padding[0])
        end_padding = max(features_padding[1], targets_padding[1])
        print(f"start_padding: {start_padding} end_padding: {end_padding}")

        features_all = []
        targets_all = []

        for data_item in data_items:
            points_features = self.features_extractor.get_points_features(data_item)
            if features_all == []:
                features_all = [[] for _ in points_features]
            elif len(features_all) != len(points_features):
                raise ValueError(f"Dimensions should be the same: "
                                 f"features_all: {len(features_all)} points_features: {len(points_features)}")
            points_target = self.targets_extractor.get_points_target(data_item)

            for idx, point_features in enumerate(points_features):
                point_features_cut = safe_slice(point_features, start_padding, end_padding)
                features_all[idx].extend(point_features_cut)

            targets_all.extend(safe_slice(points_target, start_padding, end_padding))

        print(f"features_all: {len(features_all)} x {len(features_all[0])} targets_all: {len(targets_all)}")
        return (features_all, targets_all)
