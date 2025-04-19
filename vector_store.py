import os
from typing import List
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
import json

class VectorStore:
    def __init__(self, persist_directory: str = "data/chroma"):
        self.persist_directory = persist_directory
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        self.vector_store = self._load_or_create_db()

    def _load_or_create_db(self):
        return Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )

    def process_pdf(self, file_path: str) -> List[str]:
        loader = PyPDFLoader(file_path)
        pages = loader.load()
        texts = self.text_splitter.split_documents(pages)
        return texts

    def add_documents(self, file_path: str):
        texts = self.process_pdf(file_path)
        self.vector_store.add_documents(texts)
        self.vector_store.persist()
        return True

    def search(self, query: str, k: int = 5):
        return self.vector_store.similarity_search(query, k=k) 