from flask import Flask, request, redirect, g, render_template, session
import pickledb
import utils.apib as genetic
import utils.spotify_reqs as sp

db = pickledb.load('population.db',True)
app = Flask(__name__)
app.secret_key = "that's a secret i'll never tell"

# ----------------------- AUTH API PROCEDURE -------------------------

@app.route('/auth/')
def auth():
    return redirect(sp.AUTH_URL)

@app.route("/callback/")
def callback():
    auth_token = request.args['code']
    auth_header = sp.authorize(auth_token)
    session['auth_header'] = auth_header
    return playlist()

def valid_token(resp):
    return resp is not None and not 'error' in resp

# -------------------------- API REQUESTS ----------------------------

@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html')

@app.route('/playlist')
def playlist():
    if 'auth_header' in session:
        auth_header = session['auth_header']
        initial_playlist = sp.get_todays_top(auth_header)
        features = [sp.get_features(track['track']['id'], auth_header) for track in initial_playlist]
        population = genetic.init_population(initial_playlist, features, 'indie-pop')
        db.set('population', population)
        if valid_token(initial_playlist):
            return render_template('playlist.html', pop=population)
    return render_template('home.html')

@app.route('/newplay', methods=["GET", "POST"])
def mating():
    if 'auth_header' in session:
        auth_header = session['auth_header']
        new_fits = request.form.getlist('rate')
        population = db.get('population')
        population = genetic.fitness(new_fits, population)
        children = genetic.mating(population, sp, auth_header)
        new_pop = genetic.update_population(population, children)
        return render_template('playlist.html', pop=new_pop)

@app.route('/download')
def download():
    if 'auth_header' in session:
        auth_header =  session['auth_header']
        playlist_id = sp.create_playlist(auth_header)
        population = db.get('population')
        sp.fill_playlist(population, playlist_id, auth_header)
        return render_template('download.html')

if __name__ == '__main__':
    app.run(debug=True)