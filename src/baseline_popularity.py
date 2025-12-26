import pandas as pd
ratings = pd.read_csv("data/raw/ratings.csv")
movies = pd.read_csv("data/raw/movies.csv")
data=ratings.merge(movies, on="movieId")
movie_stats = (
    data.groupby("movieId")
    .agg(num_ratings=("rating", "count"), avg_rating=("rating", "mean"), title=("title", "first"))
    .reset_index()
)
MIN_RATINGS= 45
popular_movies=movie_stats[movie_stats["num_ratings"]>= MIN_RATINGS]
popular_movies = popular_movies.sort_values(
    by=["num_ratings", "avg_rating"],
    ascending=[False, False]
)
top10 = popular_movies.head(10)
top10["avg_rating"] = top10["avg_rating"].round(1)
print(top10.to_string(index=False))