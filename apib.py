from random import sample, randint
from dna import DNA

def gen_individual(track, features):
    ind = {}

    ind['id'] = track['id']
    ind['popularity'] = track['popularity']
    ind['danceability'] = features['danceability']
    ind['energy'] = features['energy']
    ind['loudness'] = features['loudness']
    ind['mode'] = features['mode']
    ind['speechiness'] = features['speechiness']
    ind['acousticness'] = features['acousticness']
    ind['instrumentalness'] = features['instrumentalness']
    ind['liveness'] = features['liveness']
    ind['valence'] = features['valence']
    ind['tempo'] = features['tempo']

    return ind

def init_population(n_parents, initial_playlist, features_dict):
    population = []

    for i in range(n_parents):
        indiv = gen_individual(initial_playlist['items'][i]['track'], features_dict[i])
        population.append((-1, indiv)) # -1 is the initial fit
    
    return population

def fitness():
    # tem que fazer né kk
    pass

def select_index(probs, k):
    for i in range(probs):
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
        parents.append(population[pi])
        sample.remove(population[pi])
    
    return parents

def nsfw(parents):
    child = DNA()

