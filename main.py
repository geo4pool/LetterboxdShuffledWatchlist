from collect_data import get_all_data
from recommend_films import recommend_films

"""
What I ran to get all the data that I used:

get_all_data("jakobboewer", 10000)  # ran with max_users=10000 but did not get that far (also csv written to was FINAL_RATING_DATA.csv)
split_data("FINAL_RATING_DATA.csv")
"""

print(recommend_films("jakobboewer"))  # prints a watchlist that is a (disjoint) union of a real subset of a watchlist and recommendations based on the watchlist