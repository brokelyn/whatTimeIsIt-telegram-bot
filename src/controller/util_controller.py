import telegram
import time
import datetime
from datetime import timedelta

from entity.message import Message
from entity.user import User
from entity.group import Group
from entity.score import Score
from repo.message_repo import MessageRepo
from repo.user_repo import UserRepo
from repo.group_repo import GroupRepo
from repo.statistic_repo import StatisticRepo
from repo.score_repo import ScoreRepo
from service.time_service import TimeService
import service.event_service as EventService


class UtilController:

    @staticmethod
    def format_timedelta(duration: timedelta) -> str:
        """Format a timedelta as 'Xh Ym Zs' format."""
        total_seconds = int(duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        parts = []
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")
        if seconds > 0 or len(parts) == 0:
            parts.append(f"{seconds}s")
        
        return " ".join(parts)

    @staticmethod
    async def handle_text_msg(update, context):
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
                    await UtilController.wrong_time_action(update, context)

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
    async def message_time(update, context):
        rpl_msg = update.message.reply_to_message
        group = GroupRepo.get_or_none(rpl_msg.chat.id)
        if group is None:
            timezone = "UTC"
        else:
            timezone = group.timezone

        if rpl_msg:
            msg_time = TimeService.datetime_correct_tz(rpl_msg.date, timezone)
            await rpl_msg.reply_text("Timestamp of this message is:\n" +
                               msg_time.strftime('%H:%M:%S at %d.%m.%Y'))
        else:
            update.message.reply_text("Please reply to a message to see it's timestamp")

    @staticmethod
    async def ban_action(context, restrict_duration: timedelta, group: Group, msg):
        try:
            if not group.invite_link:
                group.invite_link = await context.bot.export_chat_invite_link(msg.chat.id)
                GroupRepo.save(group)

            duration_str = UtilController.format_timedelta(restrict_duration)
            ban_text = "Your ban will last for " + duration_str + \
                    "\n\nUse this link " + group.invite_link + \
                    " to join after your ban has expired."

            send_msg = await context.bot.send_message(chat_id=msg.chat.id,
                                                text=ban_text + "\n\nYou will be banned in 21 seconds")
            time.sleep(1)

            for i in range(20, 5, -5):
                await context.bot.edit_message_text(chat_id=msg.chat.id,
                                            message_id=send_msg.message_id,
                                            text=ban_text + "\n\nYou will be banned in " + str(i) + " seconds")
                time.sleep(5)  # dont update too often due to flood protection

            await context.bot.edit_message_text(chat_id=msg.chat.id, message_id=send_msg.message_id, text=ban_text)

            await context.bot.ban_chat_member(chat_id=msg.chat.id,
                                        user_id=msg.from_user.id,
                                        until_date=restrict_duration.total_seconds())

        except telegram.error.BadRequest:
            await context.bot.send_message(msg.chat.id, text="Not enough rights to ban group member")

    @staticmethod
    async def permission_action(context, restrict_duration: timedelta, msg):
        try:
            permissions = telegram.ChatPermissions()
            permissions.no_permissions()

            duration_str = UtilController.format_timedelta(restrict_duration)
            await context.bot.send_message(msg.chat.id, text="Your rights will be removed for "
                                                       + duration_str + "!")

            time.sleep(1)

            unban_date = datetime.datetime.utcnow() + restrict_duration

            await context.bot.restrict_chat_member(chat_id=msg.chat.id,
                                             user_id=msg.from_user.id,
                                             until_date=unban_date,
                                             permissions=permissions)

        except telegram.error.BadRequest:
            await context.bot.send_message(msg.chat.id, text="Not enough rights to restrict permission of group member")

    @staticmethod
    async def minus_point_action(context, group: Group, msg):
        msg_text_time = TimeService.is_valid_time(msg.text)
        msg_ts_corrected = TimeService.datetime_correct_tz(msg.date, group.timezone)
        msg_date = int(msg_ts_corrected.strftime('%Y%m%d'))

        # Get or create statistic and score
        statistic = StatisticRepo.get_or_create(group.id, msg_text_time)

        # Get existing score or create new one
        existing_scores = ScoreRepo.scores_to_stat(statistic)
        user_score = None
        for score in existing_scores:
            if score.user.id == msg.from_user.id:
                user_score = score
                break

        if user_score is None:
            user = User(id=msg.from_user.id, username=msg.from_user.username,
                       first_name=msg.from_user.first_name,
                       last_name=msg.from_user.last_name)
            UserRepo.create_if_not_exist(user)
            user_score = Score(user=user.id, stat=statistic, points=0, date=0)

        # Apply penalty every time
        old_points = user_score.points
        user_score.points = max(0, user_score.points - 1)
        user_score.date = msg_date
        ScoreRepo.save(user_score)

        if old_points == 0:
            penalty_text = ("The time *" + str(msg.text) + "* is wrong from *" +
                          msg.from_user.first_name + "*.\n" +
                          "Message timestamp: *" + msg_ts_corrected.strftime('%H:%M:%S') + "* \n\n" +
                          "You already have 0 points, can't go lower!")
        else:
            penalty_text = ("The time *" + str(msg.text) + "* is wrong from *" +
                          msg.from_user.first_name + "*.\n" +
                          "Message timestamp: *" + msg_ts_corrected.strftime('%H:%M:%S') + "* \n\n" +
                          "New score for time *" + str(msg_text_time) + "*: " +
                          str(old_points) + " - 1 = " + str(user_score.points) + " points")

        await context.bot.send_message(msg.chat.id, text=penalty_text, parse_mode=telegram.constants.ParseMode.MARKDOWN)

    @staticmethod
    async def wrong_time_action(update, context):
        msg = update.message
        group = GroupRepo.get_or_create(msg.chat.id, msg.chat.title)
        msg_ts_corrected = TimeService.datetime_correct_tz(msg.date, group.timezone)
        await msg.reply_text("The time '" + str(msg.text) + "' is wrong from " +
                       msg.from_user.first_name + ".\n" + "Message timestamp:  "
                       + msg_ts_corrected.strftime('%H:%M:%S'))

        restrict_duration = TimeService.timedelta_until_next_day()

        if group.violation_action == "ban":
            await UtilController.ban_action(context, restrict_duration, group, msg)

        elif group.violation_action == "permission":
            await UtilController.permission_action(context, restrict_duration, msg)

        elif group.violation_action == "minus_point":
            await UtilController.minus_point_action(context, group, msg)

        elif group.violation_action == "none":
            await context.bot.send_message(msg.chat.id,
                                     text="Lucky you! Punishement is disabled!")
