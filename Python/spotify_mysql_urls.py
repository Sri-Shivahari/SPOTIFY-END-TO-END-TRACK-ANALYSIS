import re
import time
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import mysql.connector
from requests.exceptions import ReadTimeout, ConnectionError

# Set up Spotify API credentials with extended timeout
sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id = 'Client_id',
        client_secret = 'client_secret'
    ),
    requests_timeout=30  # Increase timeout to 30 seconds
)

# MySQL Database Connection
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'spotify_db'
}

# Connect to the database
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Read track URLs from file
file_path = "track_urls.txt"
with open(file_path, 'r') as file:
    track_urls = [line.strip() for line in file if line.strip()]

# Retry and insert logic
def fetch_track_with_retry(track_id, max_retries=3, delay=5):
    for attempt in range(max_retries):
        try:
            return sp.track(track_id)
        except (ReadTimeout, ConnectionError) as e:
            print(f"[Retry {attempt+1}/{max_retries}] Timeout for track {track_id}: {e}")
            time.sleep(delay)
        except Exception as e:
            print(f"❌ Unexpected error on track {track_id}: {e}")
            return None
    return None  # After retries failed

# Process each URL
for track_url in track_urls:
    try:
        # Extract track ID
        track_id_match = re.search(r'track/([a-zA-Z0-9]+)', track_url)
        if not track_id_match:
            print(f"⚠️ Invalid URL format: {track_url}")
            continue
        track_id = track_id_match.group(1)

        # Fetch track info with retries
        track = fetch_track_with_retry(track_id)
        if track is None:
            print(f"❌ Failed to fetch track: {track_url}")
            continue

        # Extract and insert data
        track_data = {
            'Track Name': track['name'],
            'Artist': track['artists'][0]['name'],
            'Album': track['album']['name'],
            'Popularity': track['popularity'],
            'Duration (minutes)': track['duration_ms'] / 60000
        }

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

        print(f"Inserted: {track_data['Track Name']} by {track_data['Artist']}")

    except Exception as e:
        print(f" Error processing {track_url}: {e}")

# Finalize
cursor.close()
connection.close()
print("\n All tracks processed.")
