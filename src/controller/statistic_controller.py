import telegram

from src.controller.base_controller import send_typing_action
from src.repo.statistic_repo import StatisticRepo
from src.service.statistic_service import StatisticService


class StatisticController:

    @staticmethod
    @send_typing_action
    def stats(update, context):
        if len(context.args) <= 0:
            StatisticController.stats_keyboard(update, context)
        else:
            try:
                time = int(context.args[0])
            except ValueError:
                context.bot.send_message(chat_id=update.message.chat_id,
                                         text="Please enter a valid time")
                return
            if 0 < time < 2359:
                StatisticController.stats_to_time(update.message.chat_id,
                                                  context.bot, time)
            else:
                context.bot.send_message(chat_id=update.message.chat_id,
                                         text="Time to big or small")

    @staticmethod
    def stats_keyboard(update, context):
        custom_keyboard = [['/stats 1337'], ['/stats 1111', '/stats 2222']]
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Choose a stat or request a custom by '/stats <4 numbers>'",
                                 reply_markup=telegram.ReplyKeyboardMarkup(custom_keyboard))

    @staticmethod
    def stats_to_time(chat_id, bot, time: int):
        statistic = StatisticRepo.get_or_create(time)
        StatisticService.calc_stats(statistic)
        dict = StatisticService.extract_scores(statistic)
        board_text = StatisticService.html_presentation(dict, statistic.time)
        bot.send_message(chat_id=chat_id, text=board_text, parse_mode="HTML",
                         reply_markup=telegram.ReplyKeyboardRemove())

    @staticmethod
    def stats_by_job(context):
        StatisticController.stats_to_time(context.job.context, context.bot, int(context.job.name))
