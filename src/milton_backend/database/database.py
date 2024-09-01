import sqlite3

from milton_backend.config.config import Config

config = Config()

class Database:
    _instance = None
    _conn = None
    _cursor = None
    _path = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._initialize()
        return cls._instance

    @classmethod
    def _initialize(cls):
        cls._path = config.get(key='database_path')
        cls._conn = sqlite3.connect(cls._path)
        cls._cursor = cls._conn.cursor()        
