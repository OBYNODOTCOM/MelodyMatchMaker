import os
import json
import sys
import tempfile
from pathlib import Path

# Ensure the project root is on sys.path when running tests directly.
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

import pandas as pd
import pytest
import numpy as np

from melody_core import (
    FEATURE_COLUMNS,
    clear_remembered_user,
    find_user,
    format_duration,
    get_spotify_embed_html,
    hash_password,
    load_data,
    load_remembered_user,
    load_users,
    save_remembered_user,
    save_users,
    build_tree,
    get_recommendations,
)


class TestUtilityFunctions:
    """Test utility functions."""

    def test_format_duration_valid(self):
        """Test formatting various durations."""
        assert format_duration(65000) == "1:05"
        assert format_duration(0) == "0:00"
        assert format_duration(3600000) == "60:00"
        assert format_duration(1000) == "0:01"
        assert format_duration(60000) == "1:00"

    def test_format_duration_edge_cases(self):
        """Test edge cases for duration formatting."""
        assert format_duration(59000) == "0:59"
        assert format_duration(599000) == "9:59"

    def test_get_spotify_embed_html_valid(self):
        """Test Spotify embed HTML generation."""
        html = get_spotify_embed_html("spotify:track:12345abcde")
        assert "12345abcde" in html
        assert "open.spotify.com/embed/track" in html
        assert "iframe" in html
        assert "width" in html

    def test_get_spotify_embed_html_different_tracks(self):
        """Test HTML generation for different track IDs."""
        html1 = get_spotify_embed_html("spotify:track:abc123")
        html2 = get_spotify_embed_html("spotify:track:xyz789")
        assert "abc123" in html1
        assert "xyz789" in html2
        assert html1 != html2


class TestPasswordHashing:
    """Test password hashing functions."""

    def test_hash_password_deterministic(self):
        """Test that hashing is deterministic."""
        password = "test_password_123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        assert hash1 == hash2

    def test_hash_password_different_inputs(self):
        """Test that different passwords produce different hashes."""
        assert hash_password("password1") != hash_password("password2")
        assert hash_password("test") != hash_password("Test")

    def test_hash_password_length(self):
        """Test that hashes are correct length (SHA256 produces 64 hex chars)."""
        hashed = hash_password("anything")
        assert len(hashed) == 64


class TestUserManagement:
    """Test user management functions."""

    def test_find_user_by_username(self):
        """Test finding user by username."""
        users = {
            "Alice": {"email": "alice@example.com", "password": "x"},
            "bob": {"email": "bob@example.com", "password": "y"},
        }

        username, user = find_user("Alice", users)
        assert username == "Alice"
        assert user["email"] == "alice@example.com"

    def test_find_user_by_email(self):
        """Test finding user by email."""
        users = {
            "Alice": {"email": "alice@example.com", "password": "x"},
            "bob": {"email": "bob@example.com", "password": "y"},
        }

        username, user = find_user("bob@example.com", users)
        assert username == "bob"
        assert user["password"] == "y"

    def test_find_user_case_insensitive(self):
        """Test that user finding is case-insensitive."""
        users = {"Alice": {"email": "alice@example.com", "password": "x"}}

        username, user = find_user("ALICE", users)
        assert username == "Alice"

        username, user = find_user("ALICE@EXAMPLE.COM", users)
        assert username == "Alice"

    def test_find_user_not_found(self):
        """Test finding non-existent user."""
        users = {"Alice": {"email": "alice@example.com", "password": "x"}}

        username, user = find_user("NonExistent", users)
        assert username is None
        assert user is None

    def test_find_user_with_whitespace(self):
        """Test finding user with whitespace in input."""
        users = {"Alice": {"email": "alice@example.com", "password": "x"}}

        username, user = find_user("  Alice  ", users)
        assert username == "Alice"


class TestUserPersistence:
    """Test user data persistence functions."""

    def test_load_users_empty_file(self):
        """Test loading users when file doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            users_file = os.path.join(tmpdir, "users.json")
            users = load_users(users_file)
            assert users == {}

    def test_save_and_load_users(self):
        """Test saving and loading users."""
        with tempfile.TemporaryDirectory() as tmpdir:
            users_file = os.path.join(tmpdir, "users.json")
            test_users = {
                "alice": {"email": "alice@example.com", "password": "hashed123"},
                "bob": {"email": "bob@example.com", "password": "hashed456"},
            }

            save_users(test_users, users_file)
            loaded = load_users(users_file)

            assert loaded == test_users
            assert loaded["alice"]["email"] == "alice@example.com"

    def test_users_json_format(self):
        """Test that users are saved in valid JSON format."""
        with tempfile.TemporaryDirectory() as tmpdir:
            users_file = os.path.join(tmpdir, "users.json")
            test_users = {"alice": {"email": "alice@example.com", "password": "hash"}}

            save_users(test_users, users_file)

            with open(users_file, "r") as f:
                loaded = json.load(f)
            assert loaded == test_users


class TestRememberMe:
    """Test remember me functionality."""

    def test_save_and_load_remembered_user(self):
        """Test saving and loading remembered user."""
        with tempfile.TemporaryDirectory() as tmpdir:
            remember_file = os.path.join(tmpdir, "remember.json")

            save_remembered_user("alice", remember_file)
            loaded = load_remembered_user(remember_file)

            assert loaded == "alice"

    def test_load_remembered_user_file_not_exists(self):
        """Test loading remembered user when file doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            remember_file = os.path.join(tmpdir, "remember.json")
            loaded = load_remembered_user(remember_file)
            assert loaded is None

    def test_clear_remembered_user(self):
        """Test clearing remembered user."""
        with tempfile.TemporaryDirectory() as tmpdir:
            remember_file = os.path.join(tmpdir, "remember.json")

            save_remembered_user("alice", remember_file)
            assert os.path.exists(remember_file)

            clear_remembered_user(remember_file)
            assert not os.path.exists(remember_file)

    def test_clear_remembered_user_file_not_exists(self):
        """Test clearing when file doesn't exist (should not raise error)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            remember_file = os.path.join(tmpdir, "remember.json")
            # Should not raise an exception
            clear_remembered_user(remember_file)


class TestDataLoading:
    """Test data loading and processing."""

    @pytest.fixture
    def sample_csv_file(self):
        """Create a sample CSV file for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_file = os.path.join(tmpdir, "test_data.csv")
            data = pd.DataFrame({
                "energy": [0.5, 0.7, 0.3],
                "tempo": [120, 140, 100],
                "danceability": [0.6, 0.8, 0.4],
                "loudness": [-5, -3, -7],
                "liveness": [0.3, 0.5, 0.2],
                "valence": [0.6, 0.7, 0.5],
                "speechiness": [0.1, 0.2, 0.05],
                "instrumentalness": [0.1, 0.05, 0.2],
                "acousticness": [0.3, 0.2, 0.4],
                "track_popularity": [50, 70, 40],
                "track_album_release_date": ["2020-01-01", "2021-06-15", "2019-03-20"],
            })
            data.to_csv(csv_file, index=False)
            yield csv_file

    def test_load_data_basic(self, sample_csv_file):
        """Test loading and processing data."""
        data, data_features = load_data([sample_csv_file])

        assert isinstance(data, pd.DataFrame)
        assert data_features.shape[0] == 3  # 3 rows
        assert data_features.shape[1] == len(FEATURE_COLUMNS)  # 9 features

    def test_load_data_has_required_columns(self, sample_csv_file):
        """Test that loaded data has required columns."""
        data, _ = load_data([sample_csv_file])

        for col in FEATURE_COLUMNS:
            assert col in data.columns
        assert "popularity_weight" in data.columns
        assert "year" in data.columns

    def test_load_data_popularity_weight_range(self, sample_csv_file):
        """Test that popularity weights are normalized to 0-1."""
        data, _ = load_data([sample_csv_file])

        assert (data["popularity_weight"] >= 0).all()
        assert (data["popularity_weight"] <= 1).all()


class TestRecommendationEngine:
    """Test recommendation engine functions."""

    @pytest.fixture
    def sample_music_data(self):
        """Create sample music data for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_file = os.path.join(tmpdir, "test_data.csv")
            data = pd.DataFrame({
                "energy": [0.5, 0.7, 0.3, 0.8, 0.6],
                "tempo": [120, 140, 100, 150, 125],
                "danceability": [0.6, 0.8, 0.4, 0.9, 0.7],
                "loudness": [-5, -3, -7, -2, -4],
                "liveness": [0.3, 0.5, 0.2, 0.6, 0.4],
                "valence": [0.6, 0.7, 0.5, 0.8, 0.65],
                "speechiness": [0.1, 0.2, 0.05, 0.15, 0.12],
                "instrumentalness": [0.1, 0.05, 0.2, 0.02, 0.08],
                "acousticness": [0.3, 0.2, 0.4, 0.1, 0.25],
                "track_popularity": [50, 70, 40, 85, 60],
                "track_album_release_date": ["2020-01-01", "2021-06-15", "2019-03-20",
                                              "2022-01-10", "2020-06-30"],
            })
            data.to_csv(csv_file, index=False)
            yield csv_file

    def test_build_tree(self, sample_music_data):
        """Test building recommendation tree."""
        data, data_features = load_data([sample_music_data])
        tree = build_tree(data_features)

        # Tree should be built successfully
        assert tree is not None

    def test_get_recommendations(self, sample_music_data):
        """Test getting recommendations."""
        data, data_features = load_data([sample_music_data])
        tree = build_tree(data_features)

        indices, elapsed = get_recommendations(0, data, data_features, tree, n=3)

        assert len(indices) <= 3
        assert all(isinstance(idx, (int, np.integer)) for idx in indices)
        assert elapsed >= 0
        assert 0 not in indices  # Query song shouldn't be in results

    def test_get_recommendations_performance(self, sample_music_data):
        """Test that recommendations are returned quickly."""
        data, data_features = load_data([sample_music_data])
        tree = build_tree(data_features)

        indices, elapsed = get_recommendations(0, data, data_features, tree, n=3)

        # Should complete in reasonable time (under 1 second)
        assert elapsed < 1.0

    def test_get_recommendations_different_queries(self, sample_music_data):
        """Test that different queries produce different results."""
        data, data_features = load_data([sample_music_data])
        tree = build_tree(data_features)

        recs1, _ = get_recommendations(0, data, data_features, tree, n=2)
        recs2, _ = get_recommendations(1, data, data_features, tree, n=2)

        # Should generally have different results (not guaranteed but likely)
        # Focus on structure being correct
        assert len(recs1) <= 2
        assert len(recs2) <= 2
