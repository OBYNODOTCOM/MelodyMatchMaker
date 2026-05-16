import sys
from pathlib import Path

# Ensure the project root is on sys.path when running the file directly.
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

import pytest

from melody_core import build_tree, get_recommendations, load_data


def test_recommendation_performance_threshold():
    data, data_features = load_data()
    tree = build_tree(data_features)

    # Choose a track index that exists in the dataset.
    track_index = 0
    recs, elapsed = get_recommendations(track_index, data, data_features, tree, n=10)

    assert len(recs) == 10
    assert elapsed < 1.0, f"Recommendation generation is too slow: {elapsed:.2f}s"
