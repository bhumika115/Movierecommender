import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Load data
# -----------------------------
ratings = pd.read_csv("data/raw/ratings.csv")
movies = pd.read_csv("data/raw/movies.csv")

print("\n--- Preview (ratings) ---")
print(ratings.head())

print("\n--- Preview (movies) ---")
print(movies.head())

# -----------------------------
# Basic dataset stats
# -----------------------------
n_users = ratings["userId"].nunique()
n_movies = ratings["movieId"].nunique()
n_ratings = len(ratings)

sparsity = 1 - (n_ratings / (n_users * n_movies))

print("\n--- Dataset Stats ---")
print(f"Users: {n_users}")
print(f"Movies: {n_movies}")
print(f"Ratings: {n_ratings}")
print(f"Sparsity: {sparsity:.4f} (higher means more empty user-movie matrix)")

# -----------------------------
# Rating distribution
# -----------------------------
plt.figure()
ratings["rating"].hist(bins=10)
plt.title("Rating Distribution")
plt.xlabel("Rating")
plt.ylabel("Count")
plt.show()

# -----------------------------
# Ratings per user (cold-start insight)
# -----------------------------
ratings_per_user = ratings.groupby("userId").size()

plt.figure()
ratings_per_user.hist(bins=50)
plt.title("Ratings per User")
plt.xlabel("Number of Ratings")
plt.ylabel("Users")
plt.show()

# -----------------------------
# Ratings per movie (long-tail insight)
# -----------------------------
ratings_per_movie = ratings.groupby("movieId").size()

plt.figure()
ratings_per_movie.hist(bins=50)
plt.title("Ratings per Movie")
plt.xlabel("Number of Ratings")
plt.ylabel("Movies")
plt.show()

# -----------------------------
# Top 10 most-rated movies table
# -----------------------------
movie_stats = (
    ratings.groupby("movieId")
    .agg(num_ratings=("rating", "count"), avg_rating=("rating", "mean"))
    .reset_index()
    .merge(movies[["movieId", "title"]], on="movieId", how="left")
    .sort_values(by=["num_ratings", "avg_rating"], ascending=[False, False])
)

top10_most_rated = movie_stats.head(10).copy()
top10_most_rated["avg_rating"] = top10_most_rated["avg_rating"].round(2)

print("\n--- Top 10 Most-Rated Movies ---")
print(top10_most_rated[["title", "num_ratings", "avg_rating"]].to_string(index=False))
