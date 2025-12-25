import pandas as pd
import matplotlib.pyplot as plt

ratings=pd.read_csv("data/raw/ratings.csv")
movies=pd.read_csv("data/raw/movies.csv")

print(ratings.head())
print(movies.head())

n_users=ratings['userId'].nunique()
n_movies=ratings['movieId'].nunique()
n_ratings=len(ratings)
sparsity = 1 - (n_ratings / (n_users * n_movies))
ratings["rating"].hist(bins=10)
plt.title("Rating Distribution")
plt.xlabel("Rating")
plt.ylabel("Count")
plt.show()
ratings_per_user=ratings.groupby("userId").size()
ratings_per_user.hist(bins=50)
ratings_per_movie = ratings.groupby("movieId").size()
movie_stats = (
    ratings.groupby("movieId")
    .agg(num_ratings=("rating", "count"), avg_rating=("rating", "mean"))
    .reset_index()
)
merge(movies[["movieId", "title"]], on="movieId", how="left") # type: ignore
sort_values(by=["num_ratings", "avg_rating"], ascending=[False, False]) # type: ignore
top15_most_rated = movie_stats.head(15).copy()
top15_most_rated["avg_rating"] = top15_most_rated["avg_rating"].round(2)
print(top15_most_rated[["title", "num_ratings", "avg_rating"]].to_string(index=False))
