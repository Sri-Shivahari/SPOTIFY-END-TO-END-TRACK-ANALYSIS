import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify credentials
client_id = 'Client_id'
client_secret = 'client_secret'

# Authenticate
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
))

# Playlist URL
playlist_url = "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M"
playlist_id = playlist_url.split("/")[-1].split("?")[0]  # Extract clean ID

# Fetch tracks from playlist
results = sp.playlist_tracks(playlist_id)
tracks = results['items']

# Handle pagination
while results['next']:
    results = sp.next(results)
    tracks.extend(results['items'])

# Extract URLs
track_urls = []
for item in tracks:
    try:
        url = item['track']['external_urls']['spotify']
        track_urls.append(url)
    except:
        continue

# Write to file
with open("track_url.txt", "w") as file:
    for url in track_urls:
        file.write(url + "\n")

print(f"Extracted {len(track_urls)} track URLs to 'track_url.txt'")
