import os
import chromadb
from threading import Lock
from src.milton_backend.database.utils import get_top_series_by_popularity

class ChromaDBClient:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    chroma_persist_directory = os.path.join(os.path.dirname(__file__), "chroma_db")
                    cls._instance = chromadb.PersistentClient(path=chroma_persist_directory)
        return cls._instance

