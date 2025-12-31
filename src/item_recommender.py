import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

ratings = pd.read_csv("data/raw/ratings.csv")
movies = pd.read_csv("data/raw/movies.csv")

USER_ID = 1
TOP_N = 10
LIKE_THERSHOLD=3.5

rating_matrix = ratings.pivot_table(
    index="userId", 
    columns="movieId", 
    values="rating",
    fill_value=0
)

movie_ids = rating_matrix.columns
sim_matrix = cosine_similarity(rating_matrix.T)
sim_df = pd.DataFrame(sim_matrix, index=movie_ids, columns=movie_ids)

user_ratings = ratings[ratings["userId"] == USER_ID]
liked_movies = user_ratings[user_ratings["rating"] >= LIKE_THERSHOLD]

if liked_movies.empty:
    print("No liked movies found for the user.")
    raise SystemExit
seen_movie_ids = set(user_ratings["movieId"])
scores = {}
for _, row in liked_movies.iterrows():
    movie_id = row["movieId"]
    rating = row["rating"]
    similar_movies = sim_df[movie_id]
    for sim_movie_id, similarity in similar_movies.items():
        if sim_movie_id in seen_movie_ids:
            continue
        if sim_movie_id not in scores:
            scores[sim_movie_id] = 0.0
        scores[sim_movie_id] += similarity * (rating - LIKE_THERSHOLD)
sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
top_n_scores = sorted_scores[:TOP_N]
recommendations = pd.DataFrame(top_n_scores, columns=["movieId", "score"])
recommendations["score"] = recommendations["score"].round(2)
recommendations = recommendations.merge(movies[["movieId", "title", "genres"]], on="movieId")
print(recommendations[["movieId", "title", "genres", "score"]].to_string(index=False))



