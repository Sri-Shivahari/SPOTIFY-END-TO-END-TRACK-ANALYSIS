import re
import time
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
from requests.exceptions import ReadTimeout, ConnectionError

# Spotify API credentials
client_id = 'Client_id'
client_secret = 'client_secret'

# Setup Spotify client with longer timeout
sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret),
    requests_timeout=30  # increase timeout
)

# MySQL connection settings
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'spotify_db'
}

# Extract track ID from URL
track_url = "https://open.spotify.com/track/003vvx7Niy0yvhvHt4a68B"
track_id = re.search(r'track/([a-zA-Z0-9]+)', track_url).group(1)

# --- Retry fetching track with timeout handling ---
max_retries = 3
retry_delay = 5  # seconds

for attempt in range(1, max_retries + 1):
    try:
        track = sp.track(track_id)
        break  # success
    except (ReadTimeout, ConnectionError) as e:
        print(f"[Retry {attempt}/{max_retries}] Request failed: {e}")
        if attempt == max_retries:
            print("❌ Failed to fetch track after multiple attempts.")
            exit(1)
        time.sleep(retry_delay)

# Prepare data for insertion
track_data = {
    'Track Name': track['name'],
    'Artist': track['artists'][0]['name'],
    'Album': track['album']['name'],
    'Popularity': track['popularity'],
    'Duration (minutes)': track['duration_ms'] / 60000
}

# Connect to MySQL and insert
try:
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    insert_query = """
        INSERT INTO spotify_tracks_ (track_name, artist, album, popularity, duration_minutes)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (
        track_data['Track Name'],
        track_data['Artist'],
        track_data['Album'],
        track_data['Popularity'],
        track_data['Duration (minutes)']
    ))
    connection.commit()

    print(f"Track '{track_data['Track Name']}' by {track_data['Artist']} inserted into the database.")

except mysql.connector.Error as db_err:
    print(f"Database error: {db_err}")
finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()
