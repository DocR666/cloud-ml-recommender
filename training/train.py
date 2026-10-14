import pickle
from pathlib import Path

import numpy as np
from sklearn.model_selection import train_test_split

from data_loader import load_ratings, load_movies
from evaluate import rmse, baseline_rmse

N_FACTORS = 20   # size of each user's / movie's "taste profile"
EPOCHS = 20      # passes over the training data
LR = 0.01        # how big each adjustment step is
REG = 0.05       # penalty that stops the numbers from growing too large
MODEL_PATH = Path(__file__).parent / "model.pkl"

def train_mf(train_df, test_df, n_users, n_items):
    rng = np.random.default_rng(42)
    P = rng.normal(0, 0.1, (n_users, N_FACTORS))  # user taste profiles
    Q = rng.normal(0, 0.1, (n_items, N_FACTORS))  # movie style profiles
    bu = np.zeros(n_users)                        # per-user bias (generous/harsh rater)
    bi = np.zeros(n_items)                        # per-movie bias (generally liked/disliked)
    mu = train_df["rating"].mean()
    model = {"mu": mu, "bu": bu, "bi": bi, "P": P, "Q": Q}

    users = train_df["user_idx"].values
    items = train_df["item_idx"].values
    ratings = train_df["rating"].values

    for epoch in range(1, EPOCHS + 1):
        for j in rng.permutation(len(ratings)):
            u, i, r = users[j], items[j], ratings[j]
            pred = mu + bu[u] + bi[i] + P[u] @ Q[i]
            err = r - pred

            bu[u] += LR * (err - REG * bu[u])
            bi[i] += LR * (err - REG * bi[i])
            p_old = P[u].copy()
            P[u] += LR * (err * Q[i] - REG * P[u])
            Q[i] += LR * (err * p_old - REG * Q[i])

        if epoch % 5 == 0 or epoch == 1:
            print(f"epoch {epoch:2d}  test RMSE = {rmse(model, test_df):.4f}")
    return model


def main():
    ratings = load_ratings()
    movies = load_movies()

    # MovieLens ids start at 1; convert to 0-based array positions
    ratings["user_idx"] = ratings["user_id"] - 1
    ratings["item_idx"] = ratings["item_id"] - 1
    n_users = ratings["user_id"].max()
    n_items = ratings["item_id"].max()

    train_df, test_df = train_test_split(ratings, test_size=0.2, random_state=42)
    print(f"{len(train_df)} training ratings, {len(test_df)} test ratings")
    print(f"Baseline (always guess the average) RMSE = {baseline_rmse(train_df, test_df):.4f}")

    model = train_mf(train_df, test_df, n_users, n_items)

    # Everything the API needs goes in one file: model, titles, and what each user has already rated
    model["titles"] = movies.sort_values("item_id")["title"].tolist()
    model["rated"] = ratings.groupby("user_idx")["item_idx"].apply(list).to_dict()
    model["counts"] = (
        ratings.groupby("item_idx").size()
        .reindex(range(int(n_items)), fill_value=0).to_numpy()
    )
    

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    print(f"Saved model to {MODEL_PATH}")


if __name__ == "__main__":
    main()