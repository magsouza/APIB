import sys
import spotipy
import spotipy.util as util

class Spotify:

    def __init__(self):
        self.username = sys.argv[1] 
        self.scope = 'playlist-modify-public'
        self.token = util.prompt_for_user_token(username=self.username, scope=self.scope)
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
        recommended = self.sp.recommendations(seed_artists=s_artists, seed_genres=s_genres, seed_tracks=s_tracks, limit=1, **targets)

        return recommended
