import json, base64, requests, sys
from random import randint

SPOTIFY_API_BASE_URL = 'https://api.spotify.com'
API_VERSION = "v1"
SPOTIFY_API_URL = f"{SPOTIFY_API_BASE_URL}/{API_VERSION}"

try:
    import urllib.request, urllib.error
    import urllib.parse as urllibparse
except ImportError:
    import urllib as urllibparse

# ----------------- 1. USER AUTHORIZATION ----------------

# spotify endpoints
SPOTIFY_AUTH_BASE_URL = "https://accounts.spotify.com/{}"
SPOTIFY_AUTH_URL = SPOTIFY_AUTH_BASE_URL.format('authorize')
SPOTIFY_TOKEN_URL = SPOTIFY_AUTH_BASE_URL.format('api/token')

# client keys
with open('conf.json') as c:
    config = json.load(c)
CLIENT_ID = config['ID']
CLIENT_SECRET = config['SECRET']

# server side parameter
REDIRECT_URI = 'http://127.0.0.1:5000/callback/'
SCOPE = 'playlist-modify-public'
STATE = ''
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "client_id": CLIENT_ID
}

if sys.version_info[0] >= 3:
    URL_ARGS = "&".join([f"{key}={urllibparse.quote(val)}" for key, val in list(auth_query_parameters.items())])
else: 
    URL_ARGS = "&".join([f"{key}={urllibparse.quote(val)}" for key, val in auth_query_parameters.iteritems()])


#---------------- auth request
AUTH_URL = f"{SPOTIFY_AUTH_URL}/?{URL_ARGS}"

def authorize(auth_token):

    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI
    }
    
    if sys.version_info[0] >= 3:
        base64encoded = base64.b64encode((f"{CLIENT_ID}:{CLIENT_SECRET}").encode())
        headers = {"Authorization": f"Basic {base64encoded.decode()}"}
    else: 
        base64encoded = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}")
        headers = {"Authorization": f"Basic {base64encoded}"}

    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload,
                                 headers=headers)

    # tokens are returned to the app
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]

    # use the access token to access Spotify API
    auth_header = {"Authorization": "Bearer {}".format(access_token)}
    return auth_header

# ---------------- 2. PLAYLIST REQUEST ------------------------
playlist_id = '37i9dQZF1DXcBWIGoYBM5M'
fields = 'items(track.artists, track.id, track.name, track.popularity, track.preview_url)'
GET_PLAYLIST_TRACKS_ENDPOINT = f'{SPOTIFY_API_URL}/playlists/{playlist_id}/tracks'

def get_todays_top(auth_header):
    url = f'{GET_PLAYLIST_TRACKS_ENDPOINT}?fields={fields}'
    resp = requests.get(url, headers=auth_header).json()
    playlist = resp['items']
    rand_play = []
    rand = []
    while len(rand) < 15:
        i = randint(0, len(playlist)-1)
        if i not in rand:
            rand.append(i)
    for n in rand:
        rand_play.append(playlist[n])
    return rand_play

# ---------------- 3. FEATURES REQUEST ------------------------
GET_TRACK_FEATURES = f'{SPOTIFY_API_URL}/audio-features'

def get_features(track_id, auth_header):
    url = f'{GET_TRACK_FEATURES}/{track_id}'
    resp = requests.get(url, headers=auth_header)
    return resp.json()

# ---------------- 4. TRACK REQUEST ------------------------
GET_TRACK_RECOMMENDATIONS = f'{SPOTIFY_API_URL}/recommendations'

def get_track(features, targets, auth_header):
    s_artists = ','.join(features['s_artists'])
    s_genres = features['s_genres']
    s_tracks = ','.join(features['s_tracks'])

    url = f'{GET_TRACK_RECOMMENDATIONS}?limit=1&seed_artists={s_artists}&seed_genres={s_genres}&seed_tracks={s_tracks}'
    resp = requests.get(url, headers=auth_header)
    return resp.json()
