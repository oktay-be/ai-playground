from azure.storage.blob import BlobServiceClient
import os
# from pypdf import PdfReader, PdfWriter
# from file_processing.read_and_process import FileProcessor

# TODO: Check uploaded approved client documents to verify (sending to gpt)
# container can be APPROVED_CLIENT_DOCUMENTS or LAWS
# TODO: Support data lake storage account
class AzureOperations:
    def __init__(self, container):
        self.blob_service = BlobServiceClient(
            account_url=f"https://{os.getenv('AZURE_STORAGE_ACCOUNT')}.blob.core.windows.net", 
            credential=os.getenv('AZURE_STORAGE_KEY')
        )
        self.blob_container = self.blob_service.get_container_client(container)
        if not self.blob_container.exists():
            self.blob_container.create_container()

    def upload_blobs(self, filename):
        with open(filename, "rb") as data:
            filename = os.path.basename(filename)
            self.blob_container.upload_blob(filename, data, overwrite=True)

    def remove_blobs(self, filename):
        if self.blob_container.exists():
            filename = os.path.basename(filename)
            blob_client = self.blob_container.get_blob_client(filename)
            if blob_client.exists():
                blob_client.delete_blob()
            else:
                print("Blob does not exist")