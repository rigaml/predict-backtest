# File config.json added to Keepass entry for Tiingo
import os
import json

from utils.file_utils import get_project_root

BASE_FOLDER = get_project_root()
DATA_FOLDER = BASE_FOLDER + "/data"

# File config.json added to Keepass entry for Tiingo
SECRETS_FILE = "config.json"

API_NAME = "tiingo"
SAMPLING_INTERVALS = 15
QUOTES_DATABASE_NAME = f"stock-quotes-{API_NAME}-{SAMPLING_INTERVALS}m"
QUOTES_DATABASE_PATH_NAME = f"{DATA_FOLDER}/{QUOTES_DATABASE_NAME}.db"

RESEARCH_KEYS_FILE_PATH_NAME = F"{DATA_FOLDER}/inputs/stocks-research-keys.json"
RESEARCH_DATABASE_NAME = f"stock-research"
RESEARCH_DATABASE_PATH_NAME = f"{DATA_FOLDER}/{RESEARCH_DATABASE_NAME}.db"

DATABASE_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def get_secret(key: str):
    with open(BASE_FOLDER + "/" + SECRETS_FILE, "r", encoding="utf-8") as config_file:
        config = json.load(config_file)
        secret_value = config[f"{key}"]
    return secret_value
