
import os
import json
from logger.logger import p


REGISTRY_PATH = os.path.join("/opt/.rentdrive","Registry")

REGISTRY_FILE = '.data'
REGISTRY_FILE_PATH = os.path.join(REGISTRY_PATH, REGISTRY_FILE)


def set_registry(key, value):
    p.info("setting registry")

    try:
        os.makedirs(REGISTRY_PATH, exist_ok=True)
        registry_data = load_registry()
        registry_data[key] = value
        save_registry(registry_data)
        p.info("saved")
    except Exception as e:
        p.info(f"Error setting registry entry: {e}")

def get_registry(key):
    try:
        registry_data = load_registry()
        value = registry_data.get(key)
        return value
    except Exception as e:
        p.info(f"Error getting registry entry: {e}")
        return None

def load_registry():
    if os.path.exists(REGISTRY_FILE_PATH):
        with open(REGISTRY_FILE_PATH, 'r') as file:
            return json.load(file)
    else:
        return {}

def save_registry(data):
    with open(REGISTRY_FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)
