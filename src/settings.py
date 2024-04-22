# Executing inside a Docker container
# SELECT: "vs-code-ubuntu" or "docker" if executing inside VS Code Terminal Ubuntu or outside VS Code in Docker
import json


CURRENT_COMPUTER = "powershell"
VS_CODE_UBUNTU = "vs-code-ubuntu"
POWERSHELL = "powershell"
BASE_FOLDER = "./" if VS_CODE_UBUNTU == CURRENT_COMPUTER else "c:\\Users\\User\\AAAMio\\Projects\\riga-stock-nn\\src\\"
DATA_FOLDER = BASE_FOLDER + "/data"

API_NAME = "tiingo"
SAMPLING_INTERVALS = 15
QUOTES_DATABASE_NAME = f"stock-quotes-{API_NAME}-{SAMPLING_INTERVALS}m"
QUOTES_DATABASE_PATH_NAME = f"{DATA_FOLDER}/{QUOTES_DATABASE_NAME}.db"

RESEARCH_KEYS_FILE_PATH_NAME = F"{DATA_FOLDER}/inputs/stocks-research-keys.json"
RESEARCH_DATABASE_NAME = f"stock-research"
RESEARCH_DATABASE_PATH_NAME = f"{DATA_FOLDER}/{RESEARCH_DATABASE_NAME}.db"

DATABASE_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

def get_secret_key(api_name):
    # File config.json added to Keepass entry for Tiingo
    with open(BASE_FOLDER + "config.json", "r") as config_file:
        config = json.load(config_file)
        secret_key = config[f"{api_name}-key"]
    return secret_key