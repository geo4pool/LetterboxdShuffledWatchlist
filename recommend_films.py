import pandas as pd
from collect_data import translate_id
from get_films import get_a_shuffled_watchlist, get_user_films_to_df, get_entire_watchlist
from sklearn.neighbors import NearestNeighbors
import random


def recommend_films(username):
    training_data = pd.read_csv("training_data.csv")
    id_name_dict = translate_id(training_data)  # dictionary to translate the ids into film names
    ratings_matrix = training_data.pivot_table(index="film-id", columns="username", values="score")
    ratings_matrix = ratings_matrix[ratings_matrix.isnull().sum(axis=1) <= len(ratings_matrix.columns) - 2]  # at least 2 ratings from users in dataframe
    ratings_matrix = ratings_matrix.fillna(0)
    knn = NearestNeighbors(metric='cosine', algorithm='brute')  # cosine sijmilarity of the movies
    knn.fit(ratings_matrix.values)
    distances, indices = knn.kneighbors(ratings_matrix.values, n_neighbors=10)  # indices of which movies are most similar, i'll use distances when i look at how
    similar_dict = {}
    for i, similar in enumerate(indices):
        id_i = ratings_matrix.iloc[i].name
        similar_films = [id_name_dict[ratings_matrix.iloc[x].name] for x in
                         similar]  # list of the similar film names for each film id
        del similar_films[0]  # first similar film is (almost) always the same film
        similar_dict[id_i] = similar_films
    watchlist_shuffled = get_a_shuffled_watchlist(username)
    watched_films_df = get_user_films_to_df(username)[["film-id", "film-name"]]
    full_watchlist = get_entire_watchlist(username)
    watchlist_names = [i[1] for i in full_watchlist]  # get the real total watchlist
    similar_unknown_total = []
    for i, n in watchlist_shuffled:
        if i in similar_dict.keys():
            similar_unknown = [x for x in similar_dict[i] if x not in list(watched_films_df['film-name']) and x not in watchlist_names]
            # similar films that are *unknown* so doesn't include films watched/ in watchlist
            if len(similar_unknown) > 0:
                similar_unknown_total.append(similar_unknown[0])
    watchlist_and_unknown = [(0, x[1]) for x in watchlist_shuffled] + [(1, x) for x in similar_unknown_total]  # disjoint union of real watchlist and suggested watchlist
    random.shuffle(watchlist_and_unknown)
    return watchlist_and_unknown

