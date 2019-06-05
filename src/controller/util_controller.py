from entity.message import Message
from entity.user import User
from repo.message_repo import MessageRepo
from repo.user_repo import UserRepo
from service.time_service import TimeService


class UtilController:

    @staticmethod
    def handle_text_msg(update, context):
        UtilController.time_check(update.message)
        UtilController.persist_message(update.message)

    @staticmethod
    def time_check(message):
        if TimeService.is_valid_time(message.text)[0]:
            time_tz = TimeService.datetime_to_tz(message.date)
            msg_datetime = time_tz.strftime('%H%M')
            if not message.text == msg_datetime:
                message.reply_text("This time post seems wrong...\n"
                                   "Telegram msg time:   " + msg_datetime)

    @staticmethod
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

    @staticmethod
    def message_time(update, context):
        rpl_msg = update.message.reply_to_message
        if rpl_msg:
            msg_time = TimeService.datetime_to_tz(rpl_msg.date)
            rpl_msg.reply_text("Timestamp of this message is:\n" +
                               msg_time.strftime('%H:%M:%S %d.%m.%Y'))
        else:
            update.message.reply_text("Please reply to a message to see its timestamp")
