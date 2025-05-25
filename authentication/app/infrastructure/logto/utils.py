from app.core.config import settings
import base64
import json
from typing import Any

def get_auth_string():
    # Common pattern: Basic auth string
    credentials = f"{settings.logto_app_id}:{settings.logto_app_secret}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return f"Basic {encoded}"



def load_seed_data(filepath: str):
    with open(filepath, 'r') as f:
        return json.load(f)


def load_json_part(file_path: str, key: str) -> Any:
    """
    Load part of a JSON file by key.

    :param file_path: Path to the JSON file.
    :param key: Key whose data should be extracted from the JSON.
    :return: Data under the given key.
    :raises: FileNotFoundError, KeyError, or JSONDecodeError if any issue occurs.
    """
    with open(file_path, "r") as f:
        data = json.load(f)

    if key not in data:
        raise KeyError(f"Key '{key}' not found in JSON file '{file_path}'")

    return data[key]