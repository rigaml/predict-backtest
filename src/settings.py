# Executing inside a Docker container
# SELECT: "vs-code-ubuntu" or "docker" if executing inside VS Code Terminal Ubuntu or outside VS Code in Docker
import json


CURRENT_COMPUTER = "powershell"
BASE_FOLDER_DICT = {
    "vs-code-ubuntu": "./",
    "powershell": "c:\\Users\\User\\AAAMio\\Projects\\riga-stock-nn\\src\\"
}
BASE_FOLDER = BASE_FOLDER_DICT[CURRENT_COMPUTER]
DATA_FOLDER = BASE_FOLDER + "/data"

API_NAME = "tiingo"
SAMPLING_INTERVALS = 15
QUOTES_DATABASE_NAME = f"stock-quotes-{API_NAME}-{SAMPLING_INTERVALS}m"
QUOTES_DATABASE_PATH_NAME = f"{DATA_FOLDER}/{QUOTES_DATABASE_NAME}.db"

RESEARCH_KEYS_FILE_PATH_NAME = F"{DATA_FOLDER}/inputs/stocks-research-keys.json"
RESEARCH_DATABASE_NAME = f"stock-research"
RESEARCH_DATABASE_PATH_NAME = f"{DATA_FOLDER}/{RESEARCH_DATABASE_NAME}.db"

DATABASE_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def get_secret(key: str):
    # File config.json added to Keepass entry for Tiingo
    with open(BASE_FOLDER + "config.json", "r", encoding="utf-8") as config_file:
        config = json.load(config_file)
        secret_value = config[f"{key}"]
    return secret_value
