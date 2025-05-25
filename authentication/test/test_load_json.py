import json
import pytest
import tempfile
import os
from typing import Any

# --- The function under test ---
def load_json_part(file_path: str, key: str) -> Any:
    with open(file_path, "r") as f:
        data = json.load(f)
    if key not in data:
        raise KeyError(f"Key '{key}' not found in JSON file '{file_path}'")
    return data[key]

def test_load_json_part():
   x = load_json_part("../seed_data.json", "roles")
   print(x)

# --- Test cases using pytest ---
@pytest.fixture
def temp_json_file():
    """Fixture to create a temporary JSON file"""
    test_data = {
        "roles": [{"role": "admin"}],
        "permissions": ["read", "write"]
    }
    with tempfile.NamedTemporaryFile(delete=False, mode='w+', suffix='.json') as temp_file:
        json.dump(test_data, temp_file)
        temp_file.close()
        yield temp_file.name
        os.unlink(temp_file.name)

def test_load_valid_key(temp_json_file):
    result = load_json_part(temp_json_file, "roles")
    assert result == [{"role": "admin"}]

def test_key_not_found(temp_json_file):
    with pytest.raises(KeyError):
        load_json_part(temp_json_file, "nonexistent")

def test_invalid_json_file():
    # Create an invalid JSON file
    with tempfile.NamedTemporaryFile(delete=False, mode='w+', suffix='.json') as bad_file:
        bad_file.write("{invalid json}")
        bad_file_path = bad_file.name

    with pytest.raises(json.JSONDecodeError):
        load_json_part(bad_file_path, "roles")

    os.unlink(bad_file_path)

