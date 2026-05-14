# Music Recommendation App

This project implements a hybrid music recommendation system using Spotify data, optimized for fast recommendations under 0.5 seconds.

## Architecture

- **Hybrid Design**: Combines content-based filtering (audio features similarity) with popularity weighting
- **Algorithm**: Ball Tree from scikit-learn for efficient nearest neighbor search
- **Performance**: Recommendations generated in < 0.5 seconds

## Files

- `MelodyMatchMaker.ipynb`: Jupyter Notebook for development and testing
- `app.py`: Streamlit web app for deployment
- `high_popularity_spotify_data.csv`: High popularity Spotify tracks
- `low_popularity_spotify_data.csv`: Low popularity Spotify tracks
- `requirements.txt`: Python dependencies for deployment

## Features Used

Audio features from Spotify API:
- energy, tempo, danceability, loudness, liveness, valence, speechiness, instrumentalness, acousticness

## Display Categories

Recommendations show detailed song information:
- Song Title
- Artist
- Album
- Genre (main and subgenre)
- Release Year
- Duration (formatted as MM:SS)
- Popularity Score
- **Spotify Player** (Click "Play" to hear 30-second previews)

## Running the App

### Jupyter Notebook
1. Open `MelodyMatchMaker.ipynb` in Jupyter
2. Run all cells
3. Use the interactive widget to select tracks and get recommendations

### Streamlit Web App
1. Install dependencies: `pip install -r requirements.txt`
2. Run: `streamlit run app.py`
3. Open the provided URL in your browser

## Testing
1. Install developer dependencies: `pip install -r requirements-dev.txt`
2. Run tests: `pytest`

## Hybrid Scoring

Recommendations are scored as:
- 70% content similarity (based on audio features)
- 30% popularity weight

This ensures both musically similar and popular tracks are recommended.# MelodyMatchMaker
# MelodyMatchMaker
# MelodyMatchMaker
