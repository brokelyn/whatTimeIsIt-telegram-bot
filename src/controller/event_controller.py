import telegram
import datetime

from src.controller.base_controller import send_typing_action
from src.controller.statistic_controller import StatisticController



class EventController:

    @staticmethod
    @send_typing_action
    def add_event(update, context):
        if len(context.args) <= 0:
            EventController.add_keyboard(update, context)
        else:
            try:
                time = int(context.args[0])
            except ValueError:
                context.bot.send_message(chat_id=update.message.chat_id,
                                         text="Please enter a valid time")
                return
            if 0 < time < 2359:
                EventController.add_job(update, context, time)
            else:
                context.bot.send_message(chat_id=update.message.chat_id,
                                         text="Time to big or small")

    @staticmethod
    def add_keyboard(update, context):
        custom_keyboard = [['/addEvent 1337'], ['/addEvent 1111', '/addEvent 2222']]
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Choose event or request a custom by '/addEvent <4 numbers>'",
                                 reply_markup=telegram.ReplyKeyboardMarkup(custom_keyboard))

    @staticmethod
    def add_job(update, context, time: int):
        hours = int(str(time)[0] + str(time)[1])
        minute = (time - (hours * 100)) + 1

        if len(context.job_queue.get_jobs_by_name(str(time))) > 0:
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text="This event already exists",
                                     reply_markup=telegram.ReplyKeyboardRemove())
            return

        context.job_queue.run_repeating(StatisticController.stats_by_job, 86400,
                                        first=datetime.time(hours, minute, 10),
                                        context=update.message.chat_id,
                                        name=str(time))

        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Added event '" + str(time) + "'",
                                 reply_markup=telegram.ReplyKeyboardRemove())

    ####################################################################################

    @staticmethod
    @send_typing_action
    def remove_event(update, context):
        if len(context.args) <= 0:
            EventController.remove_keyboard(update, context)
        else:
            try:
                time = int(context.args[0])
            except ValueError:
                context.bot.send_message(chat_id=update.message.chat_id,
                                         text="Please enter a valid time")
                return
            if 0 < time < 2359:
                EventController.remove_job(update, context, str(time))
            else:
                context.bot.send_message(chat_id=update.message.chat_id,
                                         text="Time to big or small")

    @staticmethod
    def remove_keyboard(update, context):
        if len(context.job_queue.jobs()) == 0:  # todo count only not removed
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text="There are no active events")
            return

        custom_keyboard = [["/removeAllEvents"]]
        for job in context.job_queue.jobs():
            if not job.removed:
                option = ["/removeEvent " + job.name]
                custom_keyboard.append(option)
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Choose event or request a custom by '/removeEvent <4 numbers>'",
                                 reply_markup=telegram.ReplyKeyboardMarkup(custom_keyboard))

    @staticmethod
    def remove_job(update, context, job_name):
        for job in context.job_queue.get_jobs_by_name(job_name):
            job.schedule_removal()

        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Removed event '" + job_name + "'",
                                 reply_markup=telegram.ReplyKeyboardRemove())

    @staticmethod
    @send_typing_action
    def remove_all_jobs(update, context):
        for job in context.job_queue.jobs():
            job.schedule_removal()

        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Removed all events",
                                 reply_markup=telegram.ReplyKeyboardRemove())

    ####################################################################################

    @staticmethod
    def events(update, context):
        reply = "This events are active:\n"

        for job in context.job_queue.jobs():
            reply += "Event: " + job.name + "\n"
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=reply)
