# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials

# sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
#     client_id="cacb9ea1c34a41f9a9bc8a9580d2dba0",
#     client_secret="ee789656309f427285e7877f935e452b"
# ))

# playlist_id = "37i9dQZF1DXcBWIGoYBM5M"  # Example: Today's Top Hits
# results = sp.playlist_tracks(playlist_id)

# for item in results['items']:
#     track = item['track']
#     print(track['external_urls']['spotify'])


# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials

# # Spotify credentials (replace with your actual credentials)
# client_id = 'cacb9ea1c34a41f9a9bc8a9580d2dba0'
# client_secret = 'ee789656309f427285e7877f935e452b'

# # Authenticate
# sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
#     client_id=client_id,
#     client_secret=client_secret
# ))

# # Spotify playlist ID (from URL)
# # Example: https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M
# playlist_id = '37i9dQZEVXbNG2KDcFcKOF'  # "Today's Top Hits"

# # Fetch tracks
# results = sp.playlist_tracks(playlist_id)
# tracks = results['items']

# # Handle pagination (if more than 100 tracks)
# while results['next']:
#     results = sp.next(results)
#     tracks.extend(results['items'])

# # Extract Spotify URLs
# track_urls = []
# for item in tracks:
#     try:
#         track_url = item['track']['external_urls']['spotify']
#         track_urls.append(track_url)
#     except Exception:
#         continue

# # Save to track_url.txt
# with open("track_url.txt", "w") as file:
#     for url in track_urls:
#         file.write(url + "\n")

# print(f"Extracted {len(track_urls)} track URLs to 'track_url.txt'")


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
