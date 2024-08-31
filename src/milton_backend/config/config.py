import os
from dotenv import load_dotenv
from typing import Optional

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        load_dotenv()
        self._config = {}
        for key, value in os.environ.items():
            self._config[key] = value

    def get(self, key: str) -> Optional[str]:
        """
        Get the value for the given configuration key.
        
        :param key: The configuration key
        :return: The value if it exists, None otherwise
        """
        return self._config.get(key)

