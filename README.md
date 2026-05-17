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

# How to use the app
Step 1: Launch the app by tapping on the app link

Step 2: As a new user, sign up by entering your choice username, email, password, repeat password and select “create account”. A returning user would just enter the username and password only to login
Step 3: The recommender page opens automatically on sign-up or login
Step 4: You can proceed to search for any song by typing the genre, name of artist, song title or year in the search bar and select “Apply search” or “Generate recommendations”
Step 5: It displays the top-10 related songs in less than 0.005 seconds
Step 6: You can select the play button on any of the songs to play them. Note that they can all be played simultaneously
Step 7: You can repeat steps 4 to 6 to obtain new songs and your search history is saved.
Step 8: When you search for a song and it returns “No tracks found matching your search. Try a different query”,  it simply means that your song isn’t available on the app yet. 
