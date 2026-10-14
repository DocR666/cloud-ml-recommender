from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).parent / "data" / "ml-100k"


def load_ratings():
    """One row per rating: user_id, item_id, rating (1-5)."""
    return pd.read_csv(
        DATA_DIR / "u.data",
        sep="\t",
        names=["user_id", "item_id", "rating", "timestamp"],
    )


def load_movies():
    """item_id and title for every movie."""
    return pd.read_csv(
        DATA_DIR / "u.item",
        sep="|",
        header=None,
        usecols=[0, 1],
        names=["item_id", "title"],
        encoding="latin-1",
    )