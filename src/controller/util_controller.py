import telegram
import time
import datetime
from datetime import timedelta

from entity.message import Message
from entity.user import User
from entity.group import Group
from repo.message_repo import MessageRepo
from repo.user_repo import UserRepo
from repo.group_repo import GroupRepo
from service.time_service import TimeService
import service.event_service as EventService


class UtilController:

    @staticmethod
    def handle_text_msg(update, context):
        msg = update.message

        if msg.chat.type != 'private':
            msg_text_time = TimeService.is_valid_time(msg.text)
            if msg_text_time != -1:
                group = GroupRepo.get_or_create(msg.chat.id, msg.chat.title)
                time_tz = TimeService.datetime_correct_tz(msg.date, group.timezone)
                msg_datetime = time_tz.strftime('%H%M')
                if msg_text_time == int(msg_datetime):
                    if not MessageRepo.sameTimeSameUserMessageExists(msg):
                        UtilController.persist_message(msg)
                    if group.auto_events:
                        EventService.create_job(context.job_queue, group.id,msg_text_time, True)
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

        message = Message(user=user.id,
                          msg_id=msg.message_id,
                          text=msg.text,
                          time=msg.date.replace(tzinfo=None),
                          group=group.id)
        MessageRepo.create(message)

    @staticmethod
    def message_time(update, context):
        rpl_msg = update.message.reply_to_message
        group = GroupRepo.get_or_none(rpl_msg.chat.id)
        if rpl_msg:
            msg_time = TimeService.datetime_correct_tz(rpl_msg.date, group.timezone)
            rpl_msg.reply_text("Timestamp of this message is:\n" +
                               msg_time.strftime('%H:%M:%S at %d.%m.%Y'))
        else:
            update.message.reply_text("Please reply to a message to see its timestamp")

    @staticmethod
    def ban_action(context, restrict_duration: timedelta, group: Group, msg):
        try:
            if not group.invite_link:
                group.invite_link = context.bot.export_chat_invite_link(msg.chat.id)
                GroupRepo.save(group)

            ban_text = "Your ban will last for " + str(restrict_duration) + \
                    "\n\nUse this link " + group.invite_link + \
                    " to join after your ban has expired."

            send_msg = context.bot.send_message(chat_id=msg.chat.id,
                                                text=ban_text + "\n\nYou will be banned in 21 seconds")
            time.sleep(1)

            for i in range(20, 5, -5):
                context.bot.edit_message_text(chat_id=msg.chat.id,
                                            message_id=send_msg.message_id,
                                            text=ban_text + "\n\nYou will be banned in " + str(i) + " seconds")
                time.sleep(5)  # dont update too often due to flood protection

            context.bot.edit_message_text(chat_id=msg.chat.id, message_id=send_msg.message_id, text=ban_text)

            context.bot.kick_chat_member(chat_id=msg.chat.id,
                                        user_id=msg.from_user.id,
                                        until_date=restrict_duration.total_seconds())

        except telegram.error.BadRequest:
            context.bot.send_message(msg.chat.id, text="Not enough rights to ban group member")

    @staticmethod
    def permission_action(context, restrict_duration: timedelta, msg):
        try:
            permissions = telegram.ChatPermissions()
            permissions.can_send_polls = False
            permissions.can_add_web_page_previews = False
            permissions.can_change_info = False
            permissions.can_invite_users = False
            permissions.can_pin_messages = False
            permissions.can_send_media_messages = False
            permissions.can_send_messages = False
            permissions.can_send_other_messages = False

            context.bot.send_message(msg.chat.id, text="Your rights will be removed for "
                                                       + str(restrict_duration) + "!")

            time.sleep(1)

            unban_date = datetime.datetime.utcnow() + restrict_duration

            context.bot.restrict_chat_member(chat_id=msg.chat.id,
                                             user_id=msg.from_user.id,
                                             until_date=unban_date,
                                             permissions=permissions)

        except telegram.error.BadRequest:
            context.bot.send_message(msg.chat.id, text="Not enough rights to restrict permission of group member")

    @staticmethod
    def wrong_time_action(update, context):
        msg = update.message
        group = GroupRepo.get_or_create(msg.chat.id, msg.chat.title)
        msg_ts_corrected = TimeService.datetime_correct_tz(msg.date, group.timezone)
        msg.reply_text("The time '" + str(msg.text) + "' is wrong from " +
                       msg.from_user.first_name + ".\n" + "Message timestamp:  "
                       + msg_ts_corrected.strftime('%H:%M:%S'))

        restrict_duration = TimeService.timedelta_until_next_day()

        if group.violation_action == "ban":
            UtilController.ban_action(context, restrict_duration, group, msg)

        elif group.violation_action == "permission":
            UtilController.permission_action(context, restrict_duration, msg)

        elif group.violation_action == "none":
            context.bot.send_message(msg.chat.id,
                                     text="Punishement is disabled!")
