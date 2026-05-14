import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import BallTree
import time

from melody_core import (
    build_tree,
    format_duration,
    get_recommendations,
    get_spotify_embed_html,
    hash_password,
    load_data,
    load_remembered_user,
    load_users,
    save_remembered_user,
    save_users,
    clear_remembered_user,
    find_user,
)

data, data_features = load_data()

tree = build_tree(data_features)

# Streamlit app
st.title("MelodyMatchMaker")

if 'users' not in st.session_state:
    st.session_state.users = load_users()
if 'remembered_user' not in st.session_state:
    st.session_state.remembered_user = load_remembered_user()
if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None
if 'auth_message' not in st.session_state:
    st.session_state.auth_message = ''
if 'search_history' not in st.session_state:
    st.session_state.search_history = []

if st.session_state.remembered_user and not st.session_state.logged_in_user:
    if st.session_state.remembered_user in st.session_state.users:
        st.session_state.logged_in_user = st.session_state.remembered_user
        st.session_state.auth_message = "Auto logged in from remembered device."
    else:
        st.session_state.remembered_user = None
        clear_remembered_user()

if st.session_state.logged_in_user:
    page_mode = st.sidebar.radio("Page", ["Home", "Profile"])
    st.sidebar.success(f"Logged in as {st.session_state.logged_in_user}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in_user = None
        st.session_state.auth_message = "Logged out successfully."
        clear_remembered_user()
        st.rerun()
    if st.sidebar.button("Forget Me"):
        clear_remembered_user()
        st.session_state.remembered_user = None
        st.session_state.auth_message = "Remember me cleared."
else:
    auth_mode = st.sidebar.radio("Account", ["Login", "Sign Up", "Forgot Password"])

if not st.session_state.logged_in_user:
    st.write("## User Account")
    st.write("Please login or sign up to use MelodyMatchMaker.")
    with st.form(key="auth_form"):
        if auth_mode == "Login":
            identifier = st.text_input("Username or Email", key="login_id")
            password = st.text_input("Password", type="password", key="login_password")
            remember_me = st.checkbox("Remember me on this device", key="remember_me")
            submit_auth = st.form_submit_button("Login")
            if submit_auth:
                username, user = find_user(identifier, st.session_state.users)
                if user and user.get('password') == hash_password(password):
                    st.session_state.logged_in_user = username
                    st.session_state.auth_message = "Login successful."
                    if remember_me:
                        save_remembered_user(username)
                        st.session_state.remembered_user = username
                    else:
                        clear_remembered_user()
                        st.session_state.remembered_user = None
                    st.rerun()
                else:
                    st.session_state.auth_message = "Login failed. Check username/email and password."
        elif auth_mode == "Sign Up":
            new_username = st.text_input("Username", key="signup_username")
            new_email = st.text_input("Email", key="signup_email")
            new_password = st.text_input("Password", type="password", key="signup_password")
            confirm_password = st.text_input("Repeat Password", type="password", key="signup_confirm")
            remember_me = st.checkbox("Remember me on this device", key="signup_remember")
            submit_auth = st.form_submit_button("Create Account")
            if submit_auth:
                if not new_username or not new_email or not new_password:
                    st.session_state.auth_message = "All fields are required for sign up."
                elif new_username.lower() in (u.lower() for u in st.session_state.users):
                    st.session_state.auth_message = "That username is already taken."
                elif any(user.get('email', '').lower() == new_email.lower() for user in st.session_state.users.values()):
                    st.session_state.auth_message = "That email is already registered."
                elif new_password != confirm_password:
                    st.session_state.auth_message = "Passwords do not match."
                else:
                    st.session_state.users[new_username] = {
                        'email': new_email,
                        'password': hash_password(new_password)
                    }
                    save_users(st.session_state.users)
                    st.session_state.logged_in_user = new_username
                    if remember_me:
                        save_remembered_user(new_username)
                        st.session_state.remembered_user = new_username
                    else:
                        clear_remembered_user()
                        st.session_state.remembered_user = None
                    st.session_state.auth_message = "Account created and logged in."
                    st.rerun()
        else:
            reset_identifier = st.text_input("Username or Email", key="reset_id")
            reset_password = st.text_input("New Password", type="password", key="reset_password")
            reset_confirm = st.text_input("Confirm New Password", type="password", key="reset_confirm")
            submit_auth = st.form_submit_button("Reset Password")
            if submit_auth:
                username, user = find_user(reset_identifier, st.session_state.users)
                if not user:
                    st.session_state.auth_message = "No account found with that username or email."
                elif not reset_password:
                    st.session_state.auth_message = "Please enter a new password."
                elif reset_password != reset_confirm:
                    st.session_state.auth_message = "Passwords do not match."
                else:
                    st.session_state.users[username]['password'] = hash_password(reset_password)
                    save_users(st.session_state.users)
                    st.session_state.auth_message = "Password has been reset. Please log in."
    if st.session_state.auth_message:
        st.info(st.session_state.auth_message)
    st.stop()

if st.session_state.logged_in_user and st.session_state.logged_in_user:
    if page_mode == "Profile":
        st.subheader("User Profile")
        current_user = st.session_state.logged_in_user
        user_data = st.session_state.users.get(current_user, {})
        st.write(f"**Username:** {current_user}")
        st.write(f"**Email:** {user_data.get('email', 'Not set')}")
        remembered = st.session_state.remembered_user == current_user
        st.write(f"**Remember me active:** {'Yes' if remembered else 'No'}")
        st.info("Use Logout to sign out, or Forget Me to remove auto-login from this device.")
        st.markdown("---")
        st.write("### Update password")
        with st.form(key='profile_password_form'):
            current_password = st.text_input("Current Password", type="password", key="profile_current_password")
            new_password = st.text_input("New Password", type="password", key="profile_new_password")
            confirm_password = st.text_input("Confirm New Password", type="password", key="profile_confirm_password")
            submit_password = st.form_submit_button("Update Password")
            if submit_password:
                if not current_password or not new_password:
                    st.warning("Enter both current and new password.")
                elif user_data.get('password') != hash_password(current_password):
                    st.warning("Current password is incorrect.")
                elif new_password != confirm_password:
                    st.warning("New passwords do not match.")
                else:
                    st.session_state.users[current_user]['password'] = hash_password(new_password)
                    save_users(st.session_state.users)
                    st.success("Password updated successfully.")
        st.stop()

st.write("Select a song to get recommendations based on audio features and popularity.")

with st.form(key="search_form"):
    search_query = st.text_input(
        "🔍 Search by Song Title, Artist, Album, or Genre:",
        placeholder="e.g., 'Billie Eilish' or 'pop' or 'Today's Top Hits'",
        key="search_query"
    )
    submit_search = st.form_submit_button("Apply Search")

if submit_search and search_query:
    if search_query not in st.session_state.search_history:
        st.session_state.search_history.append(search_query)
    # Keep only the latest 10 searches
    st.session_state.search_history = st.session_state.search_history[-10:]

# Filter data based on search query
if search_query:
    search_lower = search_query.lower()
    filtered_data = data[
        (data['track_name'].str.lower().str.contains(search_lower, na=False)) |
        (data['track_artist'].str.lower().str.contains(search_lower, na=False)) |
        (data['track_album_name'].str.lower().str.contains(search_lower, na=False)) |
        (data['playlist_genre'].str.lower().str.contains(search_lower, na=False))
    ]
else:
    filtered_data = data

if st.session_state.search_history:
    with st.expander("Search History", expanded=True):
        for idx, item in enumerate(reversed(st.session_state.search_history), 1):
            st.write(f"{idx}. {item}")
        if st.button("Clear Search History"):
            st.session_state.search_history = []


def display_recommendations(track_idx):
    recs, elapsed = get_recommendations(track_idx, data, data_features, tree, n=10)
    selected = data.iloc[track_idx]
    st.write(f"**Selected Track:** {selected['track_name']} by {selected['track_artist']} - Album: {selected['track_album_name']}, Genre: {selected['playlist_genre']} ({selected['playlist_subgenre']}), Year: {selected['year']}, Duration: {format_duration(selected['duration_ms'])}, Popularity: {selected['track_popularity']}")
    st.markdown(get_spotify_embed_html(selected['uri']), unsafe_allow_html=True)
    st.write(f"**Recommendation Time:** {elapsed:.4f} seconds")

    st.write("**Recommendations:**")
    for i, rec_idx in enumerate(recs, 1):
        rec = data.iloc[rec_idx]
        st.write(f"{i}. {rec['track_name']} by {rec['track_artist']} - Album: {rec['track_album_name']}, Genre: {rec['playlist_genre']} ({rec['playlist_subgenre']}), Year: {rec['year']}, Duration: {format_duration(rec['duration_ms'])}, Popularity: {rec['track_popularity']}")
        st.markdown(get_spotify_embed_html(rec['uri']), unsafe_allow_html=True)

# Create track options from filtered data
track_options = [f"{row['track_name']} by {row['track_artist']}" for _, row in filtered_data.iterrows()]

if not track_options:
    st.warning("No tracks found matching your search. Try a different query.")
    selected_track = None
else:
    selected_track = st.selectbox("Choose a track:", track_options)

show_recommendations = False
if submit_search and selected_track:
    show_recommendations = True

if st.button("Get Recommendations") and selected_track:
    show_recommendations = True

if show_recommendations and selected_track:
    track_idx = filtered_data[
        (filtered_data['track_name'] + " by " + filtered_data['track_artist']) == selected_track
    ].index[0]
    display_recommendations(track_idx)
