import os
import sys
from telethon.sync import TelegramClient
from telethon.tl.functions.account import GetAuthorizationsRequest

from utils import *

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

name = getSessionName()

api_id, api_hash = loadAPIConfig(False)
client = TelegramClient(f"{CURRENT_DIR}/session/{name}", api_id, api_hash)

def getSessionInfo(client):
    msg = ""
    auths = client(GetAuthorizationsRequest())
    if __name__ == "__main__": print(auths.stringify())
    for auth in auths.authorizations:
        msg += f"""
INFORMATION:
#====================================#
Hash: {auth.hash} --> {type(auth.hash)}
is_official_app: {auth.official_app}
Country: {auth.country}
Ip: {auth.ip}
App name: {auth.app_name}
Device: {auth.device_model}
Platform: {auth.platform}
System version: {auth.system_version}
Password pending: {auth.password_pending}
#====================================#\n\n
"""
    return msg


if __name__ == "__main__":
    client.start()
    client.connect()
    print(getSessionInfo(client))


