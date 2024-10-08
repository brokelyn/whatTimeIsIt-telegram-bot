import telegram
from datetime import datetime

from service.statistic_service import StatisticService
from service.time_service import TimeService
from controller.group_controller import GroupController
from repo.group_repo import GroupRepo


class StatisticController:

    @staticmethod
    async def stats(update, context):
        if len(context.args) == 0:
            await context.bot.send_message(chat_id=update.message.chat.id, text="Usage '/stats <4 numbers>'")
        else:
            time = TimeService.is_valid_time(context.args[0])
            chat_id = update.message.chat.id
            if update.message.chat.type == 'private':
                await GroupController.group_selection(context.bot, chat_id, "stats", str(time))
            elif await StatisticController.time_check(context.bot, chat_id, chat_id, time):
                board_text = StatisticService.stats_to_time(chat_id, time)

                await context.bot.send_message(chat_id=chat_id,
                                         text=board_text,
                                         parse_mode="Markdown",
                                         reply_markup=telegram.ReplyKeyboardRemove())

    ###########################################################################
    @staticmethod
    async def stats_to_callback(update, context):
        stat_time = update.callback_query.data.split(" ")[2]
        chat_id = update.callback_query.message.chat.id
        group_id = update.callback_query.data.split(" ")[3]
        group = GroupRepo.get_or_none(group_id)

        if await StatisticController.time_check(context.bot, group_id, chat_id, stat_time):
            board_text = StatisticService.stats_to_time(int(group_id), int(stat_time))
            board_text = "Group: *" + group.title + "*\n\n" + board_text
            await update.callback_query.message.edit_text(text=board_text,
                                                    parse_mode="Markdown",
                                                    reply_markup=None)

    ###########################################################################

    @staticmethod
    async def stats_by_job(context):
        stat_time = int(context.job.name.split("/")[0])
        group_id = context.job.chat_id

        text = StatisticService.stats_to_time(group_id, stat_time)
        await context.bot.send_message(chat_id=group_id,
                                 text=text, parse_mode="Markdown",
                                 reply_markup=telegram.ReplyKeyboardRemove())

    ####################################################################################################################

    @staticmethod
    async def time_check(bot, group_id, reply_chat_id, time) -> bool:
        group = GroupRepo.get_or_none(group_id)
        current_time = TimeService.datetime_correct_tz(datetime.utcnow(), group.timezone)
        is_same_time = current_time.strftime("%H%M") == str(time)

        if not time == -1 and not is_same_time:
            return True
        elif not time == -1 and is_same_time:
            available_time = current_time.replace(minute=current_time.minute + 1).strftime("%H:%M")
            await bot.send_message(chat_id=reply_chat_id,
                             text="Ist man in kleinen Dingen nicht geduldig, "
                                  "bringt man die großen Vorhaben zum scheitern."
                                  "\n\n Die neue Statistik ist erst um "
                                  "" + available_time + " verfügbar.")
        else:
            await bot.send_message(chat_id=reply_chat_id,
                             text="Time request '" + time + "' is invalid")
        return False
