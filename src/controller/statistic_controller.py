import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import datetime

from service.statistic_service import StatisticService
from service.time_service import TimeService


class StatisticController:

    @staticmethod
    def stats(update, context):
        if len(context.args) <= 0:
            StatisticController.stats_keyboard(update, context)
        else:
            time = TimeService.is_valid_time(context.args[0])
            same_time = str(datetime.datetime.now())[11:16]
            same_time_clear = int(same_time[0:2]+same_time[3:5])
            if not time == -1 and same_time_clear!=time:
                board_text = StatisticService.stats_to_time(time)
                context.bot.send_message(chat_id=update.message.chat_id,
                                         text=board_text, parse_mode="Markdown",
                                         reply_markup=telegram.ReplyKeyboardRemove())
            if not time == -1 and same_time_clear == time:
                context.bot.send_message(chat_id=update.message.chat_id,
                                         text="Ist man in kleinen Dingen nicht geduldig, "
                                              "bringt man die großen Vorhaben zum scheitern.")
            else:
                context.bot.send_message(chat_id=update.message.chat_id,
                                         text="Time request is invalid")

    @staticmethod
    def stats_keyboard(update, context):
        inline_keyboard = [[InlineKeyboardButton("1337 statistics", callback_data="stats 1337")],
                           [InlineKeyboardButton("1111 statistics", callback_data="stats 1111")],
                           [InlineKeyboardButton("2222 statistics", callback_data="stats 2222")],
                           [InlineKeyboardButton("0000 statistics", callback_data="stats 0000")]]
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Choose a stat or request a custom by '/stats <4 numbers>'",
                                 reply_markup=InlineKeyboardMarkup(inline_keyboard))

    @staticmethod
    def stats_callback(update, context):
        stat_time = update.callback_query.data.split(" ")[1]
        board_text = StatisticService.stats_to_time(stat_time)
        update.callback_query.message.edit_text(text=board_text, parse_mode="Markdown",
                                                reply_markup=InlineKeyboardMarkup([]))

    @staticmethod
    def stats_by_job(context):
        text = StatisticService.stats_to_time(int(context.job.name))
        context.bot.send_message(chat_id=context.job.context,
                                 text=text, parse_mode="Markdown",
                                 reply_markup=telegram.ReplyKeyboardRemove())
