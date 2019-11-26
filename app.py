from flask import Flask, request, redirect, g, render_template, session
import utils.spotify_reqs as spotify

app = Flask(__name__)
app.secret_key = "that's a secret i'll never tell"

# ----------------------- GENETIC ALGORITHM CODE -------------------------




# ----------------------- AUTH API PROCEDURE -------------------------

@app.route('/auth')
def auth():
    return redirect(spotify.AUTH_URL)

@app.route("/callback/")
def callback():
    auth_token = request.args['code']
    auth_header = spotify.authorize(auth_token)
    session['auth_header'] = auth_header
    return playlist()

def valid_token(resp):
    return resp is not None and not 'error' in resp

# -------------------------- API REQUESTS ----------------------------

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/playlist')
def playlist():
    return render_template('playlist.html')

if __name__ == '__main__':
    app.run(debug=True)