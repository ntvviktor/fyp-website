import torch

from .Dataset import Dataset
from ..recommender.utils import load_data
from ..recommender.CDAE import CDAE
import pandas as pd
import plotly
import plotly.graph_objs as go
import json


train_df, train_matrix, test_matrix, user_id_map, user_popularity, \
    item_id_map, item_popularity, num_users, num_items = load_data("training.json")

original_book_data = pd.read_csv("./webapp/recommender/subset_db.csv", engine="python")
user_item_df = pd.read_csv("./webapp/recommender/user_item_rating.csv", engine="python")
hidden_dim = 50

model = CDAE(num_users=num_users,
             num_items=num_items,
             hidden_dim=hidden_dim)

model.load_state_dict(torch.load('./webapp/recommender/cdae_recommender.pth'))
model.eval()


def create_plot():
    df = pd.read_csv("./webapp/recommender/model_metrics.csv")

    data = [
        go.Scatter(
            x=df['epoch'],  # assign x as the dataframe column 'x'
            y=df['Recall@5']
        )
    ]

    graph_json = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graph_json


def create_plot_2():
    df = pd.read_csv("./webapp/recommender/model_loss.csv")

    data = [
        go.Scatter(
            x=df['epoch'],  # assign x as the dataframe column 'x'
            y=df['loss']
        )
    ]

    graph_json = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graph_json
