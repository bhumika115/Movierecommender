# Movie Recommendation System (MovieLens)
# Overview
This project builds an end-to-end movie recommendation system using the MovieLens dataset.  
It starts with exploratory data analysis (EDA), then implements baseline and advanced recommender models.

## Dataset
Source: MovieLens (ml-latest-small)

- Users: 610
- Movies: 9724
- Ratings: 100836
- Sparsity: 98.31%

## EDA Insights
1. The user–movie matrix is highly sparse, meaning most users have not rated most movies.
2. Ratings are concentrated around mid-to-high values (typically 3–4), showing positive rating bias.
3. Many users have very few ratings, creating a cold-start challenge for personalization.
4. Movie ratings follow a long-tail pattern: a few movies have many ratings, while most movies have very few.
5. A popularity-based recommender is a strong baseline because some movies dominate rating counts.

## Baseline Recommender
1. A simple popularity-based recommender was built as a starting point.
2. Movies are recommended based on how many ratings they have and their average rating.
3. A minimum rating count is used so that movies with very few ratings are not recommended.
## Content based recommendendation
1. A content based recommender was implemented using movie's genres.
2. For a user , movie they rated highly are used to understand their genre preferences.
3. Each movie is represented using their genres, and new movies are recommened if it matches   the genres they are intrested in.
 



