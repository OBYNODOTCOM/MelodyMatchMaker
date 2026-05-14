import hashlib
import json
import os
import time

import numpy as np
import pandas as pd
from sklearn.neighbors import BallTree
from sklearn.preprocessing import StandardScaler

USER_STORE_FILE = 'users.json'
REMEMBER_FILE = 'remember_me.json'
FEATURE_COLUMNS = [
    'energy',
    'tempo',
    'danceability',
    'loudness',
    'liveness',
    'valence',
    'speechiness',
    'instrumentalness',
    'acousticness',
]
DEFAULT_CSV_FILES = ['high_popularity_spotify_data.csv', 'low_popularity_spotify_data.csv']


def format_duration(ms):
    seconds = ms / 1000
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}:{secs:02d}"


def get_spotify_embed_html(uri):
    track_id = uri.split(':')[-1]
    return (
        f'<iframe src="https://open.spotify.com/embed/track/{track_id}" '
        'width="100%" height="152" frameBorder="0" allowfullscreen="" '
        'allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>'
    )


def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def load_users(user_store_file=USER_STORE_FILE):
    if not os.path.exists(user_store_file):
        return {}
    with open(user_store_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_users(users, user_store_file=USER_STORE_FILE):
    with open(user_store_file, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2)


def load_remembered_user(remember_file=REMEMBER_FILE):
    if not os.path.exists(remember_file):
        return None
    with open(remember_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('username')


def save_remembered_user(username, remember_file=REMEMBER_FILE):
    with open(remember_file, 'w', encoding='utf-8') as f:
        json.dump({'username': username}, f)


def clear_remembered_user(remember_file=REMEMBER_FILE):
    if os.path.exists(remember_file):
        os.remove(remember_file)


def find_user(identifier, users):
    identifier_lower = identifier.strip().lower()
    for username, user in users.items():
        if username.lower() == identifier_lower or user.get('email', '').lower() == identifier_lower:
            return username, user
    return None, None


def load_data(csv_paths=None):
    if csv_paths is None:
        csv_paths = DEFAULT_CSV_FILES

    frames = [pd.read_csv(path) for path in csv_paths]
    data = pd.concat(frames, ignore_index=True)
    data[FEATURE_COLUMNS] = data[FEATURE_COLUMNS].fillna(data[FEATURE_COLUMNS].mean())

    scaler = StandardScaler()
    data_features = scaler.fit_transform(data[FEATURE_COLUMNS])

    data['popularity_weight'] = data['track_popularity'] / 100.0
    data['year'] = pd.to_datetime(data['track_album_release_date'], errors='coerce').dt.year

    return data, data_features


def build_tree(data_features):
    return BallTree(data_features, leaf_size=40)


def get_recommendations(track_index, data, data_features, tree, n=10):
    start_time = time.time()
    query_point = data_features[track_index].reshape(1, -1)
    distances, indices = tree.query(query_point, k=n + 1)

    distances = distances[0][1:]
    indices = indices[0][1:]

    scores = []
    for idx, dist in zip(indices, distances):
        similarity = 1 / (1 + dist)
        hybrid_score = similarity * 0.7 + data.iloc[idx]['popularity_weight'] * 0.3
        scores.append((idx, hybrid_score))

    scores.sort(key=lambda x: x[1], reverse=True)
    recommended_indices = [idx for idx, _ in scores[:n]]
    elapsed = time.time() - start_time
    return recommended_indices, elapsed
