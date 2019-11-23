class DNA:

    '''
    DNA ATTRIBUTES:
        self.id = track_dict['id']
        self.popularity = track_dict['popularity']
        self.danceability = features_dict['danceability']
        self.energy = features_dict['energy']
        self.key = features_dict['key']
        self.loudness = features_dict['loudness']
        self.mode = features_dict['mode']
        self.speechiness = features_dict['speechiness']
        self.acousticness = features_dict['acousticness']
        self.instrumentalness = features_dict['instrumentalness']
        self.liveness = features_dict['liveness']
        self.valence = features_dict['valence']
        self.tempo = features_dict['tempo']
    '''

    def __init__(self, **kwargs):
        track_dict = kwargs.get('track', {})
        features_dict = kwargs.get('feat', {})
        for key, value in features_dict.items():
            setattr(self, key, value)
        for key, value in track_dict.items():
            setattr(self, key, value)