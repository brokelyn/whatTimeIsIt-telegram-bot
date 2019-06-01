import telegram
from telegram.ext import CommandHandler, Updater

from src.controller.base_controller import send_typing_action


class ScoreController:

    @staticmethod
    @send_typing_action
    def score(update, context):
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Not supported yet")
