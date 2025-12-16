import os
from typing import List
from dotenv import load_dotenv, find_dotenv

class ConfigError(Exception):
    """Custom exception for configuration related errors."""
    pass

class AppConfig:
    """
    Configuration class that loads settings from environment variables (os.environ).
    It validates that all required parameters are present and not None.
    """
    OLLAMA_API_KEY: str
    MCP_SERVER_FILE: str
    LLM_MODEL: str
    LLM_MODEL_TEMPERATURE: float
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    MONGODB_CONNECTION_STRING: str

    # List of required environment variable keys for validation
    REQUIRED_KEYS: List[str] = [
        "OLLAMA_API_KEY",
        "MCP_SERVER_FILE",
        "LLM_MODEL",
        "LLM_MODEL_TEMPERATURE",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD",
        "DB_HOST",
        "DB_PORT",
        "MONGODB_CONNECTION_STRING"
    ]

    def __init__(self):
        """
        Loads configuration from environment variables and validates required keys.
        """
        self._load_config()
        self._validate_required_keys()

    def _load_config(self):
        """
        Loads all defined configuration attributes from os.environ.
        """
        _ = load_dotenv(find_dotenv()) # read local .env file
        # Load required parameters
        for key in self.REQUIRED_KEYS:
            # os.getenv() is used for safety, though os.environ[...] is fine if preceded by validation
            value = os.environ.get(key)
            setattr(self, key, value)
        # Example of type conversion (if needed)
        self.LLM_MODEL_TEMPERATURE: float = float(os.environ.get("LLM_MODEL_TEMPERATURE", 0.0))
        print("Configuration loaded successfully.")


    def _validate_required_keys(self):
        """
        Checks if all variables in REQUIRED_KEYS have a non-None value.
        Raises ConfigError if any required key is missing or empty.
        """
        missing_keys: List[str] | None = []
        for key in self.REQUIRED_KEYS:
            value = getattr(self, key)
            if value is None or str(value).strip() == "":
                missing_keys.append(key)

        if missing_keys:
            raise ConfigError(
                f"Configuration missing required environment variables: {', '.join(missing_keys)}. "
                f"Please set these variables."
            )