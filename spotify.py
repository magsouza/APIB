import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
from dna import DNA

class Spotify:

    def __init__(self):
        self.username = sys.argv[1] 
        self.scope = 'playlist-modify-public'
        self.token = token = util.prompt_for_user_token(username=self.username, scope=self.scope) # add scope
        self.sp = spotipy.Spotify(auth=self.token)
    
    def get_todays_top(self):
        fields = 'items(track.album.artists, track.external_urls, track.id, track.name, track.popularity)'
        playlist = self.sp.user_playlist_tracks(user='spotify', playlist_id='37i9dQZF1DXcBWIGoYBM5M', \
                    fields=fields, limit=50)
        return playlist

    def get_music_features(self, playlist):
        track_features = []
        for track in playlist:
            tf = self.sp.audio_features(track['track']['id'])[0]
            track_features.append(tf)
        
        return track_features
    
