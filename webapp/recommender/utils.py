import pickle
import torch
import pandas as pd


def load_data(data_path):
    """
    Function that load the processed data from `preprocess()` function
    arg:
        data_path: the path of the json byte representation data
    """
    with open(data_path, "rb") as f:
        data = pickle.load(f)

    (train_df, train_matrix, test_matrix, user_id_map, user_popularity,
     item_id_map, item_popularity, num_users, num_items) = \
        data["train_df"], data['train_matrix'], data['test_matrix'], data['user_id_dict'], data['user_popularity'], \
        data['item_id_dict'], data['item_popularity'], data['num_users'], data['num_items']

    return (train_df, train_matrix, test_matrix, user_id_map, user_popularity,
            item_id_map, item_popularity, num_users, num_items)


def inference(model, user_id, user_ratings_tensor, item_id_map, k=10, apply_dropout=False):
    """
    Recommend top k items for a user.
    Returns Numpy Array

    Args:
        model: The trained CDAE model.
        user_id: The user ID for which recommendations are to be made.
        user_ratings_tensor: The rating vector for the user.
        k: The number of top items to recommend, default = 10
        apply_dropout: boolean to apply dropout
    """
    # Ensure the model is in evaluation mode
    model.eval()
    # Predict the reconstruction of the input
    reconstructed_ratings = model(user_id, user_ratings_tensor, apply_dropout=apply_dropout)
    # Get the top k item indices based on the reconstructed ratings
    _, top_k_indices = torch.topk(reconstructed_ratings, k)

    # Convert the indices to a numpy array and return
    top_k_indices = top_k_indices.cpu().numpy().flatten()
    top_k_books_id = []
    for product in top_k_indices:
        for key, val in item_id_map.items():
            if product == val:
                top_k_books_id.append(key)
    df = pd.read_csv("subset_to_db.csv", engine="python")
    top_k_books_isbn = df[df.book_id.isin(top_k_books_id)]["isbn"].tolist()
    return top_k_books_isbn
