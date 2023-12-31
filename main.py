import sys
import string
import telegram
from telethon import functions
from telethon.sync import TelegramClient
from colorama import init as colorama_init
from telegram.ext import Updater, CommandHandler
from telethon.tl.functions.account import GetAuthorizationsRequest

from utils import *

api_id, api_hash, TOKEN = loadAPIConfig()


class TelegramAccountProtector:
    def __init__(self, API_ID, API_HASH, BOT_TOKEN):
        colorama_init()
        self.TOKEN = BOT_TOKEN
        self.api_id = API_ID
        self.api_hash = API_HASH

        self.my_hashes = loadSessionHashes()

        printLog("Config loaded")

        self.client = TelegramClient(f"{CURRENT_DIR}/session/{getSessionName()}", API_ID, API_HASH)
        self.bot = telegram.Bot(BOT_TOKEN)

        self.client.start()
        self.client.connect()

        self.init_auth = self.client(GetAuthorizationsRequest()).authorizations

        self.myself = self.client.get_entity("me")
        self.updater = Updater(self.TOKEN, use_context=True)
        self.dispatcher = self.updater.dispatcher

        self.bot_username = self.bot.getMe().username

        printLog("Everything is ready")

        try:
            self.bot.send_message(self.myself.id, "Bot started.")
        except telegram.error.BadRequest:
            printError(f"You need to start your bot first.\nBot's Nickname: {self.bot_username}")
            exit(1)

    def getSessionInfo(self):
        msg = ""
        auths = self.init_auth
        for auth in auths:
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

    def _list(self, update, context):
        bot = context.bot
        if update.effective_user.id == self.myself.id:
            auths = self.getSessionInfo()
            bot.send_message(update.effective_chat.id, auths)
            printCommandLog(f"{update.effective_chat.id} | {update.effective_message.text} | {update.effective_user.username}"
                            f" | {update.effective_user.first_name} | {update.effective_user.last_name}")
        else:
            bot.send_message(update.effective_chat.id, "You're not allowed to use me.")
            printWarning(f"Blocked command from {update.effective_chat.id} | {update.effective_message.text} | @{update.effective_user.username}"
                            f" | {update.effective_user.first_name} | {update.effective_user.last_name}")

    @staticmethod
    def escapeChars(word):
        word = [x for x in str(word)]
        for i, char in enumerate(word):
            if char in string.punctuation:
                word[i] = "\\" + char
        return ''.join(word)

    def getInfo(self, auth):
        info = f"*Session hash:* {self.escapeChars(auth.hash)}\n\n" \
               f"*Device model:* {self.escapeChars(auth.device_model)}\n" \
               f"*Platform:* {self.escapeChars(auth.platform)}\n" \
               f"*API id:* {self.escapeChars(auth.api_id)}\n" \
               f"*App name:* {self.escapeChars(auth.app_name)}\n" \
               f"*App version:* {self.escapeChars(auth.app_version)}\n" \
               f"*Session created at:* {self.escapeChars(auth.date_created)}\n" \
               f"*Date active:* {self.escapeChars(auth.date_active)}\n" \
               f"*IP:* {self.escapeChars(auth.ip)}\n" \
               f"*Country:* {self.escapeChars(auth.country)}\n" \
               f"*Region:* {self.escapeChars(auth.region)}\n" \
               f"Current session? {auth.current}\n" \
               f"Official app? {auth.official_app}\n" \
               f"*Password pending?* {auth.password_pending}"

        return info

    def deleteSession(self, auths, user):
        try:
            result = self.client(
                functions.account.ResetAuthorizationRequest(hash=user.hash)
            )
            if result:
                auths.remove(user)
                return True
            else:
                return False

        except Exception as e:
            printError(e)
            return False

    def main(self):
        printLog("Starting the bot")

        self.dispatcher.add_handler(CommandHandler("list", self._list))
        self.updater.start_polling()

        printLog(f"Bot @{self.bot_username} started")
        while True:
            try:
                raw_auths = self.client(GetAuthorizationsRequest())
                auths = raw_auths.authorizations
                current_session = [x for x in auths if x.hash == 0][0]
                if self.init_auth != auths and len(auths) > len(self.init_auth):
                    for user in auths:
                        if user.hash not in self.my_hashes and int(user.hash) != 0:
                            if user.ip == current_session.ip:
                                self.init_auth = auths
                                continue

                            result = self.deleteSession(auths, user)

                            self.init_auth = auths
                            self.bot.send_message(self.myself.id,
                                                  f"Someone tried to log in your account\n\nINFO:\n{self.getInfo(user)}",
                                                  parse_mode='MarkdownV2')

                            printWarning(f"Someone tried to log in your account (check the bot)")

                            if result:
                                self.bot.send_message(self.myself.id, "✅ I deleted that session for you 😉")
                                printLog(f"Session with hash {user.hash} deleted")
                            else:
                                self.bot.send_message(self.myself.id, "🚫️*WARNING*🚫️\nI was unable to delete the session 😓")
                                printWarning(f"Unable to delete the session with hash {user.hash}")

                elif self.init_auth != auths and len(auths) < len(self.init_auth):
                    self.init_auth = auths
            except KeyboardInterrupt:
                printWarning("Stopping the Updater")
                self.updater.stop()
                printError("Updater stopped")
                self.client.disconnect()
                printError("Client disconnected")
                printError("Exiting...")
                sys.exit(0)


worker = TelegramAccountProtector(api_id, api_hash, TOKEN)
worker.main()
