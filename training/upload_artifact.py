import os
from pathlib import Path

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

MODEL_PATH = Path(__file__).parent / "model.pkl"


def main():
    account = os.environ["STORAGE_ACCOUNT_NAME"]
    container = os.environ.get("MODEL_CONTAINER", "models")

    client = BlobServiceClient(
        account_url=f"https://{account}.blob.core.windows.net",
        credential=DefaultAzureCredential(),  # uses your `az login` locally
    )
    blob = client.get_blob_client(container=container, blob="model.pkl")
    with open(MODEL_PATH, "rb") as f:
        blob.upload_blob(f, overwrite=True)
    print(f"Uploaded {MODEL_PATH} to {account}/{container}/model.pkl")


if __name__ == "__main__":
    main()