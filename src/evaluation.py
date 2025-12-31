import pandas as pd

TOP_K = 10
LIKE_THRESHOLD = 3.5
MAX_USERS = 200

ratings = pd.read_csv("data/raw/ratings.csv")

movie_stats = (
    ratings.groupby("movieId")
    .agg(num_ratings=("rating", "count"), avg_rating=("rating", "mean"))
    .reset_index()
)

popular_movies = movie_stats[movie_stats["num_ratings"] >= 35]
popular_movies = popular_movies.sort_values("avg_rating", ascending=False)

popular_movie_ids = popular_movies["movieId"].tolist()

users = ratings["userId"].unique()[:MAX_USERS]

precisions = []
recalls = []

for user_id in users:
    user_ratings = ratings[ratings["userId"] == user_id]
    liked_movies = set(user_ratings[user_ratings["rating"] >= LIKE_THRESHOLD]["movieId"])

    if not liked_movies:
        continue

    seen_movies = set(user_ratings["movieId"])
    recommendations = [m for m in popular_movie_ids if m not in seen_movies][:TOP_K]

    hits = len(set(recommendations) & liked_movies)

    precision = hits / TOP_K
    recall = hits / len(liked_movies)

    precisions.append(precision)
    recalls.append(recall)

avg_precision = sum(precisions) / len(precisions)
avg_recall = sum(recalls) / len(recalls)

print(f"Precision@{TOP_K}: {avg_precision:.3f}, Recall@{TOP_K}: {avg_recall:.3f}")
