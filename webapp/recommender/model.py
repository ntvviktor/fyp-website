import torch
from ..recommender.utils import load_data
from ..recommender.CDAE import CDAE

train_df, train_matrix, test_matrix, user_id_map, user_popularity, \
     item_id_map, item_popularity, num_users, num_items = load_data("training.json")

hidden_dim = 50

model = CDAE(num_users=num_users,
             num_items=num_items,
             hidden_dim=hidden_dim)

model.load_state_dict(torch.load('./webapp/recommender/cdae_recommender.pth'))
model.eval()

