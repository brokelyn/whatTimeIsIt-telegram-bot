from functools import wraps
from telegram import ChatAction

from src.entity.message import Message
from src.entity.user import User
from src.repo.message_repo import MessageRepo
from src.repo.user_repo import UserRepo


def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return func(update, context, *args, **kwargs)

    return command_func


def persist_message(update, context):
    sender = update.message.from_user
    user = User(id=sender.id, username=sender.username,
                first_name=sender.first_name,
                last_name=sender.last_name)
    UserRepo.save_if_not_exist(user)

    msg = update.message
    message = Message(user=user.id, msg_id=msg.message_id,
                      text=msg.text, chat_id=msg.chat.id,
                      time=msg.date)
    MessageRepo.save(message)
