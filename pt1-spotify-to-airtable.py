# EXTRACT SPOTIFY FAVORITES TO AIRTABLE
# Includes advanced track features (key, mode, tempo)
# Requires Spotify and Airtable accounts + API credentials

import spotipy
import spotipy.util as util
import airtable

# INITIALIZE SPOTIFY

spot_client_id = 'XXX'
spot_client_secret = 'YYY'
spot_redirect_uri = 'http://rojwan.co'

username = 'r0ji'
scope = 'user-library-read'

token = util.prompt_for_user_token(
    username,
    scope,
    client_id=spot_client_id,
    client_secret=spot_client_secret,
    redirect_uri=spot_redirect_uri
)

if token:
    sp = spotipy.Spotify(auth=token)
else:
    print "Can't get token for ", username

# INITIALIZE AIRTABLE

at = airtable.Airtable('appXYZ', 'keyXYZ')

# GET SAVED TRACKS (default limit 20 items)
spotify_saved_tracks = sp.current_user_saved_tracks(limit=50, offset=301)
# print spotify_saved_tracks

# PUT TRACK IDS IN SEPARATE LIST (for audio features function)
spotify_track_ids = []
i = 0
for item in spotify_saved_tracks['items']:
    spotify_track_ids.append(spotify_saved_tracks['items'][i]['track']['id'])
    i += 1

# print spotify_track_ids

# GET TRACK AUDIO FEATURES
spotify_track_features = sp.audio_features(tracks=spotify_track_ids)

# print spotify_track_features

# PREPARE DATA AND SEND TO AIRTABLE
j = 0
for item in spotify_saved_tracks['items']:

    track = item['track']
    # print track

    track_spotify_id = track['id']
    # print 'Track ID: ' + track_spotify_id

    track_name = track['name']
    # print 'Track name: ' + track_name

    track_artist = track['artists'][0]['name']
    # print track_artist

    track_album = track['album']['name']
    # print track_album

    track_features = spotify_track_features[j]
    # print track_features['danceability']

    track_tempo = int(track_features['tempo'])
    # print 'Tempo ' + str(track_tempo)

    track_instrumentalness = track_features['instrumentalness']
    # print 'Instr ' + str(track_instrumentalness)

    track_key = track_features['key']
    # print 'Key ' + str(track_key)

    track_mode = track_features['mode']
    # print 'Mode ' + str(track_mode)

    # CHECK THAT BOTH LISTS MATCH (TRACK AND FEATURES)
    if track_spotify_id != track_features['id']:
        print 'Error: ID mismatch between track and features lists'
        print 'item id from track list is: ' + track_spotify_id
        print 'item id from features list is: ' + track_features['id']
        break

    j += 1

    data = {
        "Spotify ID": track_spotify_id,
        "Name": track_name,
        "Artist": track_artist,
        "Album": track_album,
        "Tempo": str(track_tempo),
        "Instrumentalness": str(track_instrumentalness),
        "Key": str(track_key),
        "Mode": str(track_mode)
    }

    print 'Adding track ' + track['name'] + ' to Airtable'

    at.create('Favorites', data)
