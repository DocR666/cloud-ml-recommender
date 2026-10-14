import pickle
import sys
from pathlib import Path

import numpy as np

MODEL_PATH = Path(__file__).parent / "model.pkl"
MIN_RATINGS = 20  # skip movies with fewer ratings than this


def load_model(path=MODEL_PATH):
    with open(path, "rb") as f:
        return pickle.load(f)


def recommend(model, user_id, n=10):
    """Top-n unseen movies for a user, ranked by predicted rating."""
    u = user_id - 1  # MovieLens ids start at 1
    if u < 0 or u >= len(model["P"]):
        raise ValueError(f"user_id must be between 1 and {len(model['P'])}")

    # predicted rating for every movie at once
    scores = model["mu"] + model["bu"][u] + model["bi"] + model["Q"] @ model["P"][u]

    # never recommend what the user has already rated
    scores[model["rated"].get(u, [])] = -np.inf
    scores[model["counts"] < MIN_RATINGS] = -np.inf

    top = np.argsort(scores)[::-1][:n]
    return [
        {
            "item_id": int(i + 1),
            "title": model["titles"][i],
            "score": round(float(min(scores[i], 5.0)), 2),
        }
        for i in top
    ]


if __name__ == "__main__":
    user = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    model = load_model()
    print(f"Top picks for user {user}:")
    for rank, rec in enumerate(recommend(model, user), start=1):
        print(f"{rank:2d}. {rec['title']}  (predicted {rec['score']})")