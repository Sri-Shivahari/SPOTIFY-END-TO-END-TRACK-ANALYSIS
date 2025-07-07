from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pandas as pd
import matplotlib.pyplot as plt
import re
import time
from requests.exceptions import ReadTimeout

# --- Spotify API credentials ---
client_id = 'Client_id'
client_secret = 'client_secret'

# --- Create Spotify client with increased timeout ---
sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    ),
    requests_timeout=20  # Increased timeout to prevent ReadTimeout
)

# --- Extract track ID from URL ---
track_url = "https://open.spotify.com/track/003vvx7Niy0yvhvHt4a68B"
track_id = re.search(r'track/([a-zA-Z0-9]+)', track_url).group(1)

# --- Try fetching track data with retry on timeout ---
try:
    track = sp.track(track_id)
except ReadTimeout:
    print("⚠️ Request timed out. Retrying in 5 seconds...")
    time.sleep(5)
    track = sp.track(track_id)

# --- Organize track data ---
track_data = {
    'Track Name': track['name'],
    'Artist': track['artists'][0]['name'],
    'Album': track['album']['name'],
    'Popularity': track['popularity'],
    'Duration (minutes)': track['duration_ms'] / 60000
}

# --- Print track info ---
print(f"\nTrack Name: {track_data['Track Name']}")
print(f"Artist: {track_data['Artist']}")
print(f"Album: {track_data['Album']}")
print(f"Popularity: {track_data['Popularity']}")
print(f"Duration: {track_data['Duration (minutes)']:.2f} minutes")

# --- Convert to DataFrame ---
df = pd.DataFrame([track_data])
print("\nTrack Data as DataFrame:")
print(df)

# --- Save to CSV (no emoji in print) ---
df.to_csv('spotify_track_data.csv', index=False)
print("\nData saved to 'spotify_track_data.csv'")  # ← emoji removed to avoid UnicodeEncodeError

# --- Plot metadata ---
features = ['Popularity', 'Duration (minutes)']
values = [track_data['Popularity'], track_data['Duration (minutes)']]

plt.figure(figsize=(8, 5))
plt.bar(features, values, color=["#1DB954", "#535353"])
plt.title(f"Track Metadata for '{track_data['Track Name']}'")
plt.ylabel('Value')
plt.tight_layout()
plt.show()
