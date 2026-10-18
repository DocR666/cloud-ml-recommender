import os
import pickle


def load_model():
    """Load the model from Blob Storage if configured, else from a local file."""
    account = os.environ.get("STORAGE_ACCOUNT_NAME")
    if account:
        from azure.identity import DefaultAzureCredential
        from azure.storage.blob import BlobServiceClient

        client = BlobServiceClient(
            account_url=f"https://{account}.blob.core.windows.net",
            credential=DefaultAzureCredential(),
        )
        blob = client.get_blob_client(
            os.environ.get("MODEL_CONTAINER", "models"),
            os.environ.get("MODEL_BLOB", "model.pkl"),
        )
        return pickle.loads(blob.download_blob().readall())

    with open(os.environ.get("MODEL_PATH", "model.pkl"), "rb") as f:
        return pickle.load(f)