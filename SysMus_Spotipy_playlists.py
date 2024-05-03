# This script provides a basic set up for connecting with the Spotify API and extracting playlist data. This
# will run through:
#    1. Set up - loading packages and authenticating API access.
#    2. Create a function for extracting data from individual playlists.
#    3. Create a function for extracting data from multiple playlists.
#    4. Run those functions, save and export your data. 
    
# This code is based on this article:
# https://towardsdatascience.com/how-to-create-large-music-datasets-using-spotipy-40e7242cc6a6



#%% 1. Set up

# First we need to add certain packages that we'll use in our program. Anaconda comes with most of what 
# we need, but we also need to install Spotipy. In the comand window (bottom right if you're using the default
# layout), type (or copy and paste) the following:
#   conda install -c conda-forge spotipy 
# While you're at it, install this other package as well - we’ll need this for our plots later:
#   conda install -c conda-forge ptitprince
# You may get a note saying that you might need to restart the kernel; to do this, press ctrl . (full stop). 

# Now, we can import our packages.
import csv
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = '0deb2c8118c84199b3d521323c83e357'
client_secret = '9284f5c45884451d8b8065515fa2b7c5'
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# This is the basic Spotipy function to retrieve information for every track in a playlist:
# sp.user_playlist_tracks('CREATOR', 'PLAYLIST_ID')
# Try this on an example:
sp.user_playlist_tracks('Spotify', '37i9dQZF1DWV7EzJMK2FUI')
# The output is quite unweildy, so we need to tidy it up.



#%% 2. 

# This will create a function for analysing a single playlist.
def analyse_playlist(creator, playlist_id):

    # Create empty dataframe
    playlist_features_list = ["artist",
        "album",
        "track_name",
        "track_id",
        "release_date",
        "popularity",
        "acousticness",
        "danceability",
        "energy",
        "key",
        "loudness",
        "mode",
        "speechiness",
        "instrumentalness",
        "liveness",
        "valence",
        "tempo",
        "duration_ms",
        "time_signature"]

    playlist_df = pd.DataFrame(columns = playlist_features_list)

    # Loop through every track in the playlist, extract features and append the features to the playlist df
    # Spotify has a limitter on how many tracks you can request at one time, but there's a way around this 
    # setting an offset and a while loop.

    n = 0

    while len(sp.user_playlist_tracks(creator, playlist_id, limit=100, offset=n)["items"]) > 0:

        playlist = sp.user_playlist_tracks(creator, playlist_id, limit=100, offset=n)["items"]
        try:
            for track in playlist:
                # Create empty dict
                playlist_features = {}
                # Get metadata
                playlist_features["artist"] = track["track"]["album"]["artists"][0]["name"]
                playlist_features["album"] = track["track"]["album"]["name"]
                playlist_features["track_name"] = track["track"]["name"]
                playlist_features["track_id"] = track["track"]["id"]
                playlist_features["release_date"] = track["track"]["album"]["release_date"]
                playlist_features["popularity"] = track["track"]["popularity"]


                # Get audio features
                audio_features = sp.audio_features(playlist_features["track_id"])[0]
                try:
                    for feature in playlist_features_list[6:]:
                        playlist_features[feature] = audio_features[feature]
                except:
                    pass

                # Concat the dfs
                track_df = pd.DataFrame(playlist_features, index = [0])
                playlist_df = pd.concat([playlist_df, track_df], ignore_index = True)
        except:
            pass

        n += 100

    return playlist_df


# Use the above function to extra data of all tracks in one playlist.
my_playlist_df = analyse_playlist('Study music selection', '7bq667TCQ77cE05DMXMaoe')

# Export to a csv file.
my_playlist_df.to_csv('study_playlist.csv')



#%% 3.

# This will create a function for analysing a dictionary (dict) or list of playlists, using the previous 
# function.
def analyse_playlist_dict(playlist_dict):

    # Loop through every playlist in the dict and analyse it
    for i, (key, val) in enumerate(playlist_dict.items()):
        playlist_df = analyse_playlist(*val)
        # Add a playlist column so that we can see which playlist a track belongs too
        playlist_df["playlist"] = key
        # Create or concat df
        if i == 0:
            playlist_dict_df = playlist_df
        else:
            playlist_dict_df = pd.concat([playlist_dict_df, playlist_df], ignore_index = True)

    return playlist_dict_df



#%% 4. 

# Now we have our functions, we just need to create our playlist dicts.
# Use the following template:
# my_playlist_dict = {'PLAYLIST_NAME' : ('PLAYLIST_CREATOR', 'PLAYLIST_ID')}

# Add as many playlists as you want, separated by a coma. Here is an example of a selection of sleep playlists:
sleep_playlists_dict = {
    'Sleep Piano Music' : ('Pryve', '7xhcF9ddiyF8Skbd1tenro'),
    'Jazz for Sleep' : ('Spotify', '37i9dQZF1DXa1rZf8gLhyz'),
    'LoFi Sleep' : ('Panda Jams', '3DP5Khm13rl3I9mQkgX6fx')
}

# Run our playlists function on the above.
sleep_playlists_df = analyse_playlist_dict(sleep_playlists_dict)

# We can add a column to these to indicate their grouping/categores.
sleep_playlists_df["category"] = "Sleep"

# Export to a csv file.
sleep_playlists_df.to_csv('sleep_playlists.csv')

# Add other playlist sets - perhaps you want to compare categories of playlists.
relaxing_playlists_dict = {
    'Ambient Relaxation' : ('Spotify', '37i9dQZF1DX3Ogo9pFvBkY'),
    'Pop Relax' : ('Spotify', '37i9dQZF1DX3SQwW1JbaFt'),
    'Relaxing Classical' : ('Filtr UK', '1ZJpJahEFst7u8njXeGFyv'),
}

# Again, run our function.
relax_playlist_df = analyse_playlist_dict(relaxing_playlists_dict)

# Add category column.
relax_playlist_df["category"] = "Relax"

# And export.
relax_playlist_df.to_csv('relax_playlists.csv')

# Let's combine them together into one dataframe.
full_playlists_df = pd.concat([sleep_playlists_df, relax_playlist_df], ignore_index = True)
full_playlists_df.to_csv('full_playlists.csv')



