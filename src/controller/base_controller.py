from functools import wraps
import dateutil.tz

from entity.message import Message
from entity.user import User
from repo.message_repo import MessageRepo
from repo.user_repo import UserRepo
from service.time_service import TimeService


def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return func(update, context, *args, **kwargs)

    return command_func


def handle_text_msg(update, context):
    time_check(update.message)
    persist_message(update.message)


def time_check(message):
    if TimeService.is_valid_time(message.text)[0]:
        time_tz = TimeService.parse_to_tz(message.date)
        msg_datetime = time_tz.strftime('%H%M')
        if not message.text == msg_datetime:
            message.reply_text("This time post seems wrong...\n"
                               "Telegram msg time:   " + msg_datetime)


def persist_message(msg):
    sender = msg.from_user
    user = User(id=sender.id, username=sender.username,
                first_name=sender.first_name,
                last_name=sender.last_name)
    UserRepo.create_if_not_exist(user)

    message = Message(user=user.id, msg_id=msg.message_id,
                      text=msg.text, chat_id=msg.chat.id,
                      time=msg.date)
    MessageRepo.create(message)
