import time

from src.controller.event_controller import EventController
from src.entity.message import Message
from src.messenger.telegram.telegram_api import TelegramApi


class MainController:
    listening = False

    def start_listening(self, timeout=10):
        self.listening = True

        while self.listening:
            new_msg = TelegramApi.receive_new()
            for msg in new_msg:
                MainController.resolve_cmd(msg)
            time.sleep(timeout)

    def stop_listening(self):
        self.listening = False

    @staticmethod
    def resolve_cmd(msg: Message):
        cmd = msg.text
        if cmd[0] == '/':
            if cmd == "/help":
                TelegramApi.send_msg(msg.chat_id, "Currently no cmds supported.")
            elif cmd == "/createEvent":
                EventController.create_event(msg)
            elif cmd == "/removeEvent":
                EventController.remove_event(msg)

            else:
                TelegramApi.send_msg(msg.chat_id, "Unknown command")
