
import pandas as pd

genres = pd.read_csv("data/genres_cleaned.csv")
movie_genres = pd.read_csv("data/movie_genres_cleaned.csv")

valid_genre_ids = set(genres["genre_id"])

unknown_genres = movie_genres[
    ~movie_genres["genre_id"].isin(valid_genre_ids)
]

print("Total genre records:", len(movie_genres))
print("Rows with unknown genre IDs:", len(unknown_genres))

if len(unknown_genres) == 0:
    print("All genre IDs are valid!")
