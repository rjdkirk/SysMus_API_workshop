# This script provides a basic set up for connecting with the Spotify API.

# First we need to add certain packages that we'll use in our program. Anaconda comes with most of what 
# we need, but we also need to add Spotipy. In the comand window (bottom right if you're using the default
# layout), type (or copy and paste) the following:
#    conda install -c conda-forge spotipy 
# Now, we can import our packages.
import csv
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# The next step is to authenticate
client_id = 'bc14dbad3a614e6bac21a603e03e343c'
client_secret = 'd6e20186fd5448f384012f42756b7f5a'
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Now we can search for data!

# This is the basic Spotipy function to retrieve information for every track in a playlist:
# sp.user_playlist_tracks('USERNAME', 'PLAYLIST_ID')
# The output you get, however, will be quite unweildy, so we need to tidy it up

# Let's try this on an example:
sp.user_playlist_tracks('Panda Jams', '3DP5Khm13rl3I9mQkgX6fx')





# This gets you audio mp3 samples.
lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'

results = sp.artist_top_tracks(lz_uri)

for track in results['tracks'][:10]:
    print('track    : ' + track['name'])
    print('audio    : ' + track['preview_url'])
    print('cover art: ' + track['album']['images'][0]['url'])
    print()
