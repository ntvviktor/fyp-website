import pickle
import time

import torch
import pandas as pd

from webapp.recommender.CDAE import CDAE
from webapp.recommender.Evaluator import Evaluator


def train_model(model: CDAE, dataset, evaluator: Evaluator, batch_size, test_batch_size, learning_rate, epochs,
                early_stop):
    """
    Function to perform training
    """
    best_epoch = -1
    best_score = None
    best_params = None
    patience = 50

    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate, weight_decay=0.01)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.1)  # optional
    loss_recorder = []
    metrics_recorder = []
    for epoch in range(1, epochs + 1):
        # train for an epoch
        epoch_start = time.time()
        loss = model.train_loop(dataset, optimizer, batch_size, verbose=False)
        train_elapsed = time.time() - epoch_start
        loss_recorder.append(float(f"{loss:.2f}"))
        # evaluate
        score = evaluator.evaluate(model, test_batch_size)
        metrics_recorder.append(dict(score))

        epoch_elapsed = time.time() - epoch_start

        score_str = ' '.join(['%s=%.4f' % (m, score[m]) for m in score])

        print(
            f"Training epoch {epoch}/{epochs}, {epoch_elapsed:.2f}, {train_elapsed:.2f} loss = {loss:.2f}, {score_str}")
        scheduler.step()
        # update if ...
        standard = 'NDCG@5'
        if best_score is None or score[standard] >= best_score[standard]:
            best_epoch = epoch
            best_score = score
            best_params = model.parameters()
            endure = 0
        else:
            endure += 1
            if early_stop and endure >= patience:
                print('Early Stop Triggered...')
                break

    print('Training Finished.')
    best_score_str = ' '.join(['%s = %.4f' % (k, best_score[k]) for k in best_score])
    print(f'Best score at epoch {best_epoch}] {best_score_str}')

    return model, loss_recorder, metrics_recorder

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


def inference(model, user_id, user_ratings_tensor, item_id_map, k=20, apply_dropout=False):
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
