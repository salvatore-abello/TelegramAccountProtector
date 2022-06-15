# TelegramAccountProtector
Protect your Telegram account from intruders!

## Features
- Check every second if an intruder has passed the login with the code
- Proceed to delete the intruder session
- All information about the intruder is sent to you. Here's an example:
 <img width="237" alt="SessionTest" src="https://user-images.githubusercontent.com/107145304/173835512-13db8975-dcd6-47c3-b3e4-e9e1a94727c9.png">

- List active sessions with `/list`
- Print all the activities in the terminal

## Setup
 - First of all, install al dependencies with `pip install -r requirements.txt`
 - Then, you need to change all values in the config file, located in `/config/config.cfg`
 - You can obtain the `id` and the `hash` from https://my.telegram.org/
 - Get the `bot_token` value from [@BotFather](https://t.me/BotFather "@BotFather")
 - Get the session hashes by running `getSessionHash.py` (You can put as many hashes as you want, but **it's necessary that the hashes belong to one account only**)
 - After you have started `getSessionHash.py` you will be asked to input the phone number of the account: a new session will be created in the `/session` directory
 - Before running the `main.py` file, you need to start the conversation with the bot (You just need to type `/start`)

## Usage
- Run the `main.py` file
- The bot will send you this message: `Bot started.`
- You can list all of your sessions with the `/list` command

**The created session will be able to eliminate intruders 24 hours after its creation**

# Warning
If anything goes wrong, the only session that will not be deleted is the one used in this app.

**I take no responsibility for any damage/data loss caused by this app.**
