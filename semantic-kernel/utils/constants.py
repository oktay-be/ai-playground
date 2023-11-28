import os
from langchain.document_loaders import CSVLoader, PDFMinerLoader, TextLoader, UnstructuredExcelLoader, Docx2txtLoader


#OPENAI_DEPLOYMENT_NAME="gpt-4-turbo"
OPENAI_DEPLOYMENT_NAME="gpt-35-turbo-16k"
OPENAI_EMBEDDING_MODEL_NAME="text-embedding-ada-002"
OPENAI_ENDPOINT=os.getenv("OPENAI_ENDPOINT")
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

DIR_PATH = 'resources'

DOCUMENT_MAP = {
    ".txt": TextLoader,
    ".md": TextLoader,
    ".py": TextLoader,
    ".pdf": PDFMinerLoader,
    ".csv": CSVLoader,
    ".xls": UnstructuredExcelLoader,
    ".xlsx": UnstructuredExcelLoader,
    ".docx": Docx2txtLoader,
    ".doc": Docx2txtLoader,
}