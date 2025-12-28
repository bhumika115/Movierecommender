import pandas as pd
import numpy as np
ratings=pd.read_csv("data/raw/ratings.csv")
movies=pd.read_csv("data/raw/movies.csv")
USER_ID=1
LIKE_THRESHOLD=3.5
TOP_N=10
genre_dummies=movies["genres"].str.get_dummies(sep="|")
genre_matrix = genre_dummies.copy()
genre_matrix["movieId"]=movies["movieId"]
genre_matrix=genre_matrix.set_index("movieId")
genre_cols=genre_dummies.columns.tolist()

user_ratings=ratings[ratings["userId"]==USER_ID]
user_likes=user_ratings[user_ratings["rating"]>=LIKE_THRESHOLD].copy()
liked_movies=user_likes.merge(movies[["movieId","title","genres"]], on="movieId")
weights= (liked_movies["rating"] - LIKE_THRESHOLD).values

liked_genre_vectors = genre_matrix.loc[liked_movies["movieId"]].values
genre_scores = np.dot(weights, liked_genre_vectors)
genre_ranking = pd.Series(genre_scores, index=genre_cols).sort_values(ascending=False)
seen_movie_ids = set(user_ratings["movieId"])
candidates = movies[~movies["movieId"].isin(seen_movie_ids)].copy()
candidates=candidates.merge(
    genre_dummies.join(movies["movieId"]), 
    on="movieId")
def compute_genre_score(row):
    score = 0.0
    for genre in genre_cols:
        if row[genre] == 1:
            score += genre_ranking.get(genre, 0)
    return score
candidates["genre_score"] = candidates.apply(compute_genre_score, axis=1)
recommendations = candidates.sort_values("genre_score", ascending=False).head(TOP_N)
print(recommendations[["movieId","title","genres","genre_score"]].to_string(index=False))