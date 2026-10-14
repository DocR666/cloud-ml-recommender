import numpy as np

MIN_RATINGS = 20  # skip movies with fewer ratings than this


def recommend(model, user_id, n=10):
    """Top-n unseen movies for a user, ranked by predicted rating."""
    u = user_id - 1  # MovieLens ids start at 1
    if u < 0 or u >= len(model["P"]):
        raise ValueError(f"user_id must be between 1 and {len(model['P'])}")

    scores = model["mu"] + model["bu"][u] + model["bi"] + model["Q"] @ model["P"][u]
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