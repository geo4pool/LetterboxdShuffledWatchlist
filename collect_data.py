from get_films import get_friend_usernames, get_user_films_to_df
import pandas as pd


def get_all_data(first_username, max_users):   # used this to get the csv file of film ratings
    df_main = pd.DataFrame(columns=['username', 'film-id', 'score', 'film-name'])
    unseen_usernames = {first_username}
    seen_usernames = set()
    while len(unseen_usernames) > 0 and len(seen_usernames) < max_users:
        username = unseen_usernames.pop()
        seen_usernames.add(username)
        print(len(seen_usernames), username)  # allows you to keep track of how many users have been seen
        following_list = get_friend_usernames(username)
        for u in following_list:
            if u not in seen_usernames:
                unseen_usernames.add(u)
        df_user = get_user_films_to_df(username)
        df_main = pd.concat([df_main, df_user], ignore_index=True)  # not sure if ignore_index True/False is better but i prefer the df as one
        df_main.to_csv("new_rating_data.csv", index=False)
    return df_main


def split_data(f):  # splits data into training and testing, haven't done testing yet
    raw_film_data = pd.read_csv(f)
    random_film_data = raw_film_data.sample(frac=1)
    split_value = int(len(random_film_data) * 0.85)
    training_data = random_film_data[:split_value]
    testing_data = random_film_data[split_value:]
    training_data.to_csv("training_data_new.csv", index=False)
    testing_data.to_csv("testing_data_new.csv", index=False)


def translate_id(df):  # creates a dictionary to translate id's to film names
    id_name = df[['film-id', 'film-name']]
    id_name = id_name.drop_duplicates(subset='film-id', keep='first', inplace=False)
    id_name_dict = dict(id_name.itertuples(index=False, name=None))
    return id_name_dict

