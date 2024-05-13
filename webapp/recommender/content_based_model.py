import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

book_data = pd.read_csv('./webapp/recommender/book2db.csv', engine="python")

tfidf = TfidfVectorizer(stop_words='english')

book_data['description'] = book_data['description'].fillna('')
tfidf_matrix = tfidf.fit_transform(book_data['description'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Construct a reverse map of indices and movie titles
indices = pd.Series(book_data.index, index=book_data['title']).drop_duplicates()
# Function that takes in movie title as input and outputs most similar movies


# def get_recommendations(title, top_k, cosine_sim=cosine_sim):
#     # Get the index of the movie that matches the title
#     try:
#         idx = indices[title]
#         # Get the pairwsie similarity scores of all books
#         sim_scores = list(enumerate(cosine_sim[idx]))
#         # Sort the books get_recommendations() based on the similarity scores
#         sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
#
#         # Get the scores of the top_k most similar books
#         sim_scores = sim_scores[1: top_k+1]
#         # Get the movie indices
#         book_indices = [i[0] for i in sim_scores]
#         # Return the top 10 most similar books
#         return book_data['isbn'].iloc[book_indices]
#     except KeyError:
#         return None


def get_recommendations(title, top_k, cosine_sim=cosine_sim):
    # Ensure title is a string and top_k is an integer
    title = str(title)
    if not isinstance(title, str) or not isinstance(top_k, int):
        return None

    try:
        idx = indices.get(title, None)
        # Ensure idx is an integer and within the cosine_sim shape
        if idx is None:
            return None

        sim_scores = list(enumerate(cosine_sim[idx]))
        # Sort the books get_recommendations() based on the similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get the scores of the top_k most similar books
        sim_scores = sim_scores[1: top_k+1]
        # Get the movie indices
        book_indices = [i[0] for i in sim_scores]
        # Return the top 10 most similar books
        return book_data['isbn'].iloc[book_indices]
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
