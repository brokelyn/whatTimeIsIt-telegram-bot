from entity.message import Message
from entity.user import User
from entity.group import Group
from repo.message_repo import MessageRepo
from repo.user_repo import UserRepo
from service.time_service import TimeService


class UtilController:

    @staticmethod
    def handle_text_msg(update, context):
        if update.message.chat.type != 'private':
            msg_text_time = TimeService.is_valid_time(update.message.text)
            if msg_text_time != -1:
                time_tz = TimeService.datetime_correct_tz(update.message.date)
                msg_datetime = time_tz.strftime('%H%M')
                if msg_text_time == int(msg_datetime):
                    if not MessageRepo.sameTimeSameUserMessageExists(update.message):
                        UtilController.persist_message(update.message)
                else:
                    UtilController.wrong_time_action(update, context)

    @staticmethod
    def persist_message(msg):
        sender = msg.from_user
        user = User(id=sender.id, username=sender.username,
                    first_name=sender.first_name,
                    last_name=sender.last_name)
        UserRepo.create_if_not_exist(user)

        group = Group(id=msg.chat.id, title=msg.chat.title)
        GroupRepo.create_if_not_exist(group)

        message = Message(user=user.id, msg_id=msg.message_id,
                          text=msg.text, chat_id=msg.chat.id,
                          time=msg.date.replace(tzinfo=None),
                          group=group.id)
        MessageRepo.create(message)

    @staticmethod
    def message_time(update):
        rpl_msg = update.message.reply_to_message
        if rpl_msg:
            msg_time = TimeService.datetime_correct_tz(rpl_msg.date)
            rpl_msg.reply_text("Timestamp of this message is:\n" +
                               msg_time.strftime('%H:%M:%S at %d.%m.%Y'))
        else:
            update.message.reply_text("Please reply to a message to see its timestamp")

    @staticmethod
    def wrong_time_action(update, context):
        msg = update.message
        msg.reply_text("The time '" + str(msg.text) + "' is wrong from " +
                           msg.from_user.first_name + " " + msg.from_user.last_name + ".\n"
                           + "Message timestamp:    " + msg.date.strftime('%H:%M:%S'))