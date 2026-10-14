import numpy as np


def predict(model, users, items):
    """Predicted ratings for arrays of (user, item) indices."""
    scores = (
        model["mu"]
        + model["bu"][users]
        + model["bi"][items]
        + (model["P"][users] * model["Q"][items]).sum(axis=1)
    )
    return np.clip(scores, 1, 5)


def rmse(model, df):
    """Root mean squared error on a dataframe of ratings."""
    preds = predict(model, df["user_idx"].values, df["item_idx"].values)
    return float(np.sqrt(np.mean((df["rating"].values - preds) ** 2)))


def baseline_rmse(train_df, test_df):
    """RMSE if we always guess the average rating. The model must beat this."""
    mean = train_df["rating"].mean()
    return float(np.sqrt(np.mean((test_df["rating"].values - mean) ** 2)))