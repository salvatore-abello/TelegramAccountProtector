import os
import json
import configparser
from colorama import Fore
from datetime import datetime

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))


def loadAPIConfig(withBot=True):
    config = configparser.ConfigParser()
    config.read(f"{CURRENT_DIR}/config/config.cfg")

    APIData = config["api-data"]
    API_ID = APIData["id"]
    API_HASH = APIData["hash"]
    BOT_TOKEN = APIData["bot_token"]

    if withBot:
        return int(API_ID), API_HASH, BOT_TOKEN
    else:
        return int(API_ID), API_HASH


def getSessionName():
    config = configparser.ConfigParser()
    config.read(f"{CURRENT_DIR}/config/config.cfg")

    return config["session"]["name"]


def loadSessionHashes():
    config = configparser.ConfigParser()
    config.read(f"{CURRENT_DIR}/config/config.cfg")

    sessions = json.loads(config["session"]["session_hashes"])
    return sessions


def printLog(msg):
    print(f"{Fore.GREEN}[{datetime.now().strftime('%d-%m-%y %H:%M:%S')}] {msg}{Fore.RESET}")


def printError(msg):
    print(f"{Fore.RED}[{datetime.now().strftime('%d-%m-%y %H:%M:%S')}] {msg}{Fore.RESET}")


def printWarning(msg):
    print(f"{Fore.YELLOW}[{datetime.now().strftime('%d-%m-%y %H:%M:%S')}] {msg}{Fore.RESET}")


def printCommandLog(msg):
    print(f"{Fore.BLUE}[{datetime.now().strftime('%d-%m-%y %H:%M:%S')}] {msg}{Fore.RESET}")
