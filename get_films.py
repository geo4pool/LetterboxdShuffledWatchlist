import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

score_translations = {"": None, "½": 0.5, "★": 1.0, "★½": 1.5, "★★": 2.0, "★★½": 2.5,
                      "★★★": 3.0, "★★★½": 3.5, "★★★★": 4.0, "★★★★½": 4.5, "★★★★★": 5.0}


def get_data(url):  # basic function to get beautiful soup object when web scraping
    res = requests.get(url)
    res = bs(res.text, "lxml")
    return res


def get_basic_stats(username, type):  # allows you to know how many films (of a certain type) there are, so you known how many pages there are to scrape later
    if type == "watchlist":  # watchlist has to be done differently
        url = f"https://letterboxd.com/{username}/watchlist"
        res = get_data(url)
        watchlist_count = res.find("span", {"class": "watchlist-count"})
        if watchlist_count is None:
            return 0
        watchlist_count = watchlist_count.text.replace("\xa0films", "")
        return int(watchlist_count)
    else:
        url = f"https://letterboxd.com/{username}/"
        res = get_data(url)
        user_stats = res.find("div", {"class": "profile-stats"})
        type_stats = user_stats.find("a", {"href": f"/{username}/{type}/"})  # e.g. number of lists, following, films etc.
        if type_stats is None:
            return 0
        else:
            return int(type_stats.find("span").text.replace(",", ""))  # gets rid of commas


def get_user_films_to_df(username):  # creates df of username, film-id, score (rating) and film-name
    film_data = []
    number_films = get_basic_stats(username, "films")
    page_number = 1
    if number_films < 1500:
        while number_films > 0:
            posters = get_film_page_data(f"{username}/films", str(page_number))
            number_films -= len(posters)  # makes sure that it doesnt search film pages that don't exist
            for p in posters:
                film_id, score, film_name = poster_to_film(p)
                if score is not None:
                    film_data.append((username, film_id, score, film_name))
            page_number += 1
    user_films_df = pd.DataFrame(film_data, columns=['username', 'film-id', 'score', 'film-name'])
    return user_films_df


def get_film_page_data(path, number):  # small function to get posters from a page
    url = f"https://letterboxd.com/{path}/page/{number}"
    res = get_data(url)
    all_posters = res.find_all("li", {"class": "poster-container"})
    return all_posters


def poster_to_film(poster, score=True):  # gets film information from posters
    film = poster.find("div", {"class": "film-poster"})
    attrs = film.attrs
    film_name = film.contents[1].attrs['alt']
    film_id = attrs['data-film-id']
    if score:
        score = poster.find("p", {"class": "poster-viewingdata"}).text
        score = score_translations[score.replace(" ", "")]
        return film_id, score, film_name
    else:
        return film_id, film_name


def get_entire_watchlist(username):  # gets all films in watchlist
    number_watchlist = get_basic_stats(username, "watchlist")
    page_number = 1
    watchlist = []
    while number_watchlist > 0:
        url = f"https://letterboxd.com/{username}/watchlist/page/{page_number}"
        res = get_data(url)
        watchlist_posters = res.find_all("li", {"class": "poster-container"})
        for p in watchlist_posters:
            film_id, film_name = poster_to_film(p, score=False)  # watchlist=True
            watchlist.append((int(film_id), film_name))
        page_number += 1
        number_watchlist -= len(watchlist_posters)
    return watchlist


def get_a_shuffled_watchlist(username):  # gets a shuffled subset of watchlist
    url = f"https://letterboxd.com/{username}/watchlist/by/shuffle/"
    res = get_data(url)
    watchlist_posters = res.find_all("li", {"class": "poster-container"})
    watchlist = []
    for p in watchlist_posters:
        film_id, film_name = poster_to_film(p, score=False)  # watchlist=True
        watchlist.append((int(film_id), film_name))
    return watchlist


def get_friend_usernames(username):  # gets all usernames for friends, useful when finding lots of film rating data and need to check other users
    # find number of following
    number_following = get_basic_stats(username, "following")

    page_number = 1
    usernames = []
    if number_following < 300:
        while number_following > 0:
            url = f"https://letterboxd.com/{username}/following/page/{page_number}"
            res = get_data(url)
            table = res.find("table", {"class": "person-table"})
            names = table.find_all("a", {"class": "name"})
            new_usernames = [i.attrs['href'][1:-1] for i in names]
            number_following -= len(new_usernames)
            usernames = usernames + [i.attrs['href'][1:-1] for i in names]  # trust me
            page_number += 1
    return usernames


def get_favourites(username):  # not used yet, finds the 0-4 "favourites" on the user profile
    res = get_data(f"https://letterboxd.com/{username}")
    favourites_section = res.find("section", {"id": "favourites"})
    posters = favourites_section.find_all("li", {"class": "poster-container"})
    favourites = []
    for p in posters:
        film_id, film_name = poster_to_film(p, score=False)
        favourites.append((int(film_id), film_name))
    return favourites


