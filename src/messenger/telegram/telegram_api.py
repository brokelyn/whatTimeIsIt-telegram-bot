import json
import subprocess
from typing import List
from urllib.parse import quote_plus

from src.entity.message import Message
from src.entity.user import User
from src.messenger.messenger_api import MessengerApi
from src.repo.bot_repo import BotRepo

bot_token = "836568720:AAHCvDJ3qLaausxazb5BVlWfKIBsaVadIZc"


class TelegramApi(MessengerApi):

    @staticmethod
    def send_msg(chat_id, msg):
        url = "https://api.telegram.org/bot" + str(bot_token)  # bot token
        url += "/sendMessage?chat_id=" + str(chat_id)
        url += "&text="

        msg = quote_plus(msg)

        subprocess.Popen(["curl", "-s", "-X", "POST", url + msg], stdout=subprocess.PIPE).stdout.read()

        print("Sent: " + msg)

    @staticmethod
    def receive_new():
        bot = BotRepo.findByName("1337")
        all_msg = TelegramApi.receive_all()
        new_messages: List[Message] = []

        for msg in all_msg:
            if bot.last_msg_id < msg.msg_id:
                new_messages.append(msg)
                bot.last_msg_id = msg.msg_id

        bot.save()
        return new_messages

    @staticmethod
    def receive_all():
        response = subprocess.Popen(
            ["curl", "-s", "-X", "POST", "https://api.telegram.org/bot" + bot_token + "/getUpdates"],
            stdout=subprocess.PIPE).stdout.read()
        messages: List[Message] = []

        try:
            data = json.loads(response)
        except:
            print("Cannot parse json")
            return None

        for i in range(len(data["result"])):
            msg_data = data["result"][i]

            if "group_chat_created" in msg_data["message"]:
                continue

            try:
                username = msg_data["message"]["from"]["username"]
                firstname = msg_data["message"]["from"]["first_name"]
                lastname = msg_data["message"]["from"]["last_name"]
                chat_id = int(msg_data["message"]["chat"]["id"])
                time = int(msg_data["message"]["date"])
                content = msg_data["message"]["text"]
                msg_id = int(msg_data["message"]["message_id"])

                user = User(username=username, first_name=firstname, last_name=lastname)
                msg = Message(msg_id=msg_id, chat_id=chat_id, user=user, time=time, text=content)
                messages.append(msg)
            except KeyError:
                print("Cannot parse message: " + str(msg_data))
                continue

        return messages
