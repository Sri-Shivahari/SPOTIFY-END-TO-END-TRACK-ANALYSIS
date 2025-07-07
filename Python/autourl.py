import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = 'Client_id'
client_secret = 'client_secret'

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id, client_secret))

playlist_id = "37i9dQZF1DXcBWIGoYBM5M"  # Today's Top Hits

try:
    # Use playlist_items instead of playlist_tracks
    results = sp.playlist_items(playlist_id, limit=100, market="US")

    track_urls = []
    for item in results["items"]:
        track = item.get("track")
        if track and track.get("external_urls") and track["external_urls"].get("spotify"):
            track_urls.append(track["external_urls"]["spotify"])

    with open("track_urls.txt", "w") as f:
        for url in track_urls:
            f.write(url + "\n")

    print("✅ Track URLs saved to track_urls.txt")

except spotipy.exceptions.SpotifyException as e:
    print(f"Spotify API error: {e}")
except Exception as e:
    print(f"General error: {e}")
