# Credit to Ole Heggli for most of this code.

# Load a few packages.
# For handling data
import pandas as pd

# plot-related libraries
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import ptitprince as pt

# For easier access to file system
import os

# Load your dataset.
dataset = pd.read_csv('sleep_playlists.csv', encoding='UTF-8', na_values='', index_col=0)

# Alt. datasets.ss
dataset = pd.read_csv('relax_playlists.csv', encoding='UTF-8', na_values='', index_col=0)
dataset = pd.read_csv('full_playlists.csv', encoding='UTF-8', na_values='', index_col=0)


# Make a folder for plots.
if not os.path.exists('Plots'):
	os.makedirs('Plots')
    
# Subset our dataset to contain only playlist, category, and the audio features.
audiofeatures = dataset[['playlist',
                         'category',
                         'popularity',
                         'danceability',
                         'energy',
                         'loudness',
                         'speechiness',
                         'acousticness',
                         'instrumentalness',
                         'liveness',
                         'valence',
                         'tempo',
                         'duration_ms']]

# We'll make raincloud plots for most of the audio features by looping through them.
features = ['popularity','danceability','energy','loudness','speechiness','acousticness',
			 'instrumentalness','liveness','valence','tempo', 'duration_ms']

# Make the plots in a loop.
for thisFeature in features:
	# Make a name for the figure
	saveName = 'Plots/PlaylistComparison-' + thisFeature + '.png'
	# draw the plot
	f, ax = plt.subplots(figsize=(7,5), dpi=300)
	pt.RainCloud(x='category', y=thisFeature, data=audiofeatures, palette='Set2', bw=.2, 
				  width_viol=.6, move=.2, ax=ax, orient='h', point_size=.75,
				  box_showfliers = False)
	# add title
	plt.suptitle(thisFeature.capitalize())
	# save the figure
	plt.savefig(saveName, bbox_inches='tight')
    
    
    
    
    
    