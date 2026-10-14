import os
import pickle


def load_model():
    """Load the trained model. For now from a local file; later from Blob Storage."""
    path = os.environ.get("MODEL_PATH", "model.pkl")
    with open(path, "rb") as f:
        return pickle.load(f)