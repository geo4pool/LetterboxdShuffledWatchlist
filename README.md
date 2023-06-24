# letterboxdshuffledwatchlist

Project uses letterboxd user ratings to suggest new films to users. Uses collaborative filtering, specifically item-item collaborative filtering- for each film (in a subset of) the watchlist, it will suggest films that the user has not seen and has not watchlisted and puts them into the list with the watchlist (similar to Spotify's smart shuffle)

Most of my time has been spent collecting data so far, because Letterboxd does not have an open API currently, so I had to web scrape all the data, after doing this, I used a simple cosine similarity algorithm to find similar films, but would like to do a better algorithm and evaluate it more in the near future.

The data has already been colected and has been stored in a CSV file. To run, just run main.py and you can insert different usernames to get different recommendations.

I think I will also do the similarity based on the user's favourite films or 5/5 rated films instead of based on the watchlist, as a user wanting to watch film X does not necessarily mean they would want to watch all 10 films most similar to film X, but if a user loves film Y, then they will probably want to watch all the films similar to film Y. However, I did it the way I did to keep the analogous nature to the Spotify smart shuffle.
