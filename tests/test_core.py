import os
import json

import pandas as pd
import pytest

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
)


def test_format_duration():
    assert format_duration(65000) == '1:05'
    assert format_duration(0) == '0:00'


def test_get_spotify_embed_html():
    html = get_spotify_embed_html('spotify:track:12345abcde')
    assert '12345abcde' in html
    assert 'open.spotify.com/embed/track' in html


def test_hash_password_changes_for_different_passwords():
    assert hash_password('password1') != hash_password('password2')
    assert hash_password('password1') == hash_password('password1')


def test_find_user_by_username_or_email(tmp_path):
    users = {
        'Alice': {'email': 'alice@example.com', 'password': 'x'},
        'bob': {'email': 'bob@example.com', 'password': 'y'},
    }

    username, user = find_user('Alice', users)
    assert username == 'Alice'
    assert user['email'] == 'alice@example.com'

    username, user = find_user('bob@example.com', users)
    assert username == 'bob'
    assert user['password'] == 'y'

    username, user = find_user('nonexistent', users)
    assert username is None
    assert user is None


def test_user_storage_round_trip(tmp_path):
    user_file = tmp_path / 'users.json'
    users = {'test': {'email': 'test@example.com', 'password': 'hash'}}
    save_users(users, user_store_file=str(user_file))
    loaded = load_users(user_store_file=str(user_file))
    assert loaded == users


def test_remembered_user_round_trip(tmp_path):
    remember_file = tmp_path / 'remember.json'
    save_remembered_user('test-user', remember_file=str(remember_file))
    assert load_remembered_user(remember_file=str(remember_file)) == 'test-user'
    clear_remembered_user(remember_file=str(remember_file))
    assert load_remembered_user(remember_file=str(remember_file)) is None


def test_load_data_succeeds(tmp_path):
    df1 = pd.DataFrame([
        {
            'energy': 0.5,
            'tempo': 120,
            'danceability': 0.7,
            'loudness': -5.0,
            'liveness': 0.1,
            'valence': 0.5,
            'speechiness': 0.05,
            'instrumentalness': 0.0,
            'acousticness': 0.1,
            'track_popularity': 50,
            'track_album_release_date': '2020-01-01',
        }
    ])
    df2 = pd.DataFrame([
        {
            'energy': 0.7,
            'tempo': 130,
            'danceability': 0.8,
            'loudness': -6.0,
            'liveness': 0.2,
            'valence': 0.6,
            'speechiness': 0.06,
            'instrumentalness': 0.01,
            'acousticness': 0.2,
            'track_popularity': 60,
            'track_album_release_date': '2021-01-01',
        }
    ])
    file1 = tmp_path / 'data1.csv'
    file2 = tmp_path / 'data2.csv'
    df1.to_csv(file1, index=False)
    df2.to_csv(file2, index=False)

    data, data_features = load_data(csv_paths=[str(file1), str(file2)])

    assert len(data) == 2
    assert data_features.shape == (2, len(FEATURE_COLUMNS))
    assert 'popularity_weight' in data.columns
    assert data.loc[0, 'year'] == 2020
    assert data.loc[1, 'year'] == 2021
