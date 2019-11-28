from random import sample, randint
import utils.spotify_reqs as sp
import json

def gen_individual(track, features, seed_genres):
    ind = {}

    ind['track_name'] = track['name']
    ind['track_id'] = track['id']
    ind['artist_name'] = track['artists'][0]['name']
    ind['artist_id'] = track['artists'][0]['id']
    ind['preview_url'] = track['preview_url']

    ind['s_artists'] = None
    ind['s_tracks'] = None
    ind['s_genres'] = seed_genres

    ind['acousticness'] = features['acousticness']
    ind['danceability'] = features['danceability']
    ind['energy'] = features['energy']
    ind['instrumentalness'] = features['instrumentalness']
    ind['liveness'] = features['liveness']
    ind['loudness'] = features['loudness']
    ind['mode'] = features['mode']
    ind['popularity'] = track['popularity']
    ind['speechiness'] = features['speechiness']
    ind['tempo'] = features['tempo']
    ind['valence'] = features['valence']

    return ind

def init_population(initial_playlist, features_dict, seed_genres):
    population = []

    for i in range(len(initial_playlist)):
        indiv = gen_individual(initial_playlist[i]['track'], features_dict[i], seed_genres)
        population.append((-1, indiv)) # -1 is the initial fit
    
    return population

def fitness(fit_values, population):
    for i in range(len(fit_values)-1, -1, -1):
        population[i] = (int(fit_values[i]), population[i][1])
    return population

def mating(population, sp, auth_header):
    children = []
    for _ in range(5):
        parents = parent_select(population)
        ch = nsfw(parents, sp, auth_header)
        children.append(ch)
    return children

def update_population(population, children):
    population = sorted(population, key=lambda i: i[0])
    new_pop = population[5:]
    for child in children:
        new_pop.append(child)
    return new_pop

def select_index(probs, k):
    for i in range(len(probs)):
        if k < probs[i]:
            return i
    return -1

def parent_select(population, n_parents=2):
    parents = []
    pop_size = len(population)

    pop_sample = sample(population, 5) # randomly select 5 individuals from population
    pop_sample.sort(key=lambda x: x[0]) # sort according to its fit
    total_fit = 0

    for i in range(2):
        for ind in pop_sample:
            total_fit += ind[0]
            total_fit *= 100
        
        prob = []
        for ind in pop_sample:
            p_ind = (ind[0]*100)/total_fit
            prob.append(p_ind)
        
        r = randint(0,99)
        pi = select_index(prob, r)
        parents.append(pop_sample[pi])
        pop_sample.remove(pop_sample[pi])
    
    return parents

def mutation(child):
    child['popularity'] = (randint(0, 100) + child['popularity']) % 100

def nsfw(parents, sp, auth_header):
    p1 = list(parents[0][1].items())[7:13]
    p2 = list(parents[1][1].items())[13:]
    seeds = [('s_artists', [parent[1]['artist_id'] for parent in parents]), 
            ('s_tracks', [parent[1]['track_id'] for parent in parents])]

    child = dict([('track_name', '_'), ('track_id', '_'), ('artist_name', '_'), 
                    ('artist_id', '_'), ('preview_url', '_')] + seeds + p1 + p2)
    mutation(child)
    targets = target_dict(child)
    track = sp.get_track(child, targets, auth_header)['tracks'][0]
    new_feat = sp.get_features(track['id'], auth_header)
    update_details(child, track, new_feat)
    return (-1, child)

def update_details(child, track, features):
    child['track_name'] = track['name']
    child['track_id'] = track['id']
    child['artist_name'] = track['artists'][0]['name']
    child['artist_id'] = track['artists'][0]['id']
    child['preview_url'] = track['preview_url']
    for k in features:
        if k in child:
            child[k] = features[k]

def target_dict(features):
    targets = {f'target_{i}': j for i, j in features.items()}
    return targets