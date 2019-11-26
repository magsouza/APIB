import sys, json, spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth

class Spotify:

    def __init__(self):
        self.token = 'BQCXNbkGW9K_2wv773VBrGywtCLyhgzMYCRI-OJSj8C5AFkKgDdJOpws1Pf1VF_HukWgZn_ggCfE_A5TfJRY3oYVf2tIrkz0RBXpCNBhhtsOCQ2kgE3WaY62-_8V3iSOS3ROSkMNlwSZL5xMYGaSmpj9NJdOFEP_U7IqZzItatc-WIJVDLA'
        self.sp = spotipy.Spotify(auth=self.token)
    
    def get_todays_top(self):
        fields = 'items(track.artists, track.id, track.name, track.popularity, track.preview_url)'
        playlist = self.sp.user_playlist_tracks(user='spotify', playlist_id='37i9dQZF1DXcBWIGoYBM5M', \
                    fields=fields, limit=10)['items']
        return playlist

    def get_features(self, track):
        tf = self.sp.audio_features(track['id'])[0]
        return tf

    def get_track(self, features, targets):
        s_artists = features['s_artists']
        s_genres = [features['s_genres']]
        s_tracks = features['s_tracks']
        recommended = self.sp.recommendations(seed_artists=s_artists, seed_genres=s_genres, \
            seed_tracks=s_tracks, limit=1, **targets)
        return recommended
