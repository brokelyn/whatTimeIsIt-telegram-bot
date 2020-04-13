import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime

from service.statistic_service import StatisticService
from service.time_service import TimeService


class StatisticController:

    @staticmethod
    def stats(update, context):
        if len(context.args) <= 0:
            StatisticController.stats_keyboard(update, context)
        else:
            time = TimeService.is_valid_time(context.args[0])
            current_time = TimeService.datetime_correct_tz(datetime.now())
            is_same_time = current_time.strftime("%H%M") == str(time)
            if not time == -1 and not is_same_time:
                board_text = StatisticService.stats_to_time(time)
                context.bot.send_message(chat_id=update.message.chat_id,
                                         text=board_text, parse_mode="Markdown",
                                         reply_markup=telegram.ReplyKeyboardRemove())
            elif not time == -1 and is_same_time:
                available_time = current_time.replace(minute=current_time.minute + 1)
                available_time = available_time.strftime("%H:%M")
                context.bot.send_message(chat_id=update.message.chat_id,
                                         text="Ist man in kleinen Dingen nicht geduldig, "
                                              "bringt man die großen Vorhaben zum scheitern."
                                              "\n\n Die neue Statistik ist erst um "
                                              "" + available_time + " verfügbar.")
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
