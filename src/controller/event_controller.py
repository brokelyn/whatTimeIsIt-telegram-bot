import telegram
from telegram import InlineKeyboardMarkup
import datetime

from controller.statistic_controller import StatisticController
from service.time_service import TimeService
from service.event_service import EventService



class EventController:

    @staticmethod
    def add_event(update, context):
        if len(context.args) <= 0:
            EventController.add_keyboard(update, context)
        else:
            time = TimeService.is_valid_time(context.args[0])
            if time[0]:
                EventController.add_job(update, context, int(context.args[0]))
            else:
                context.bot.send_message(chat_id=update.message.chat_id,
                                         text=time[1])

    @staticmethod
    def add_keyboard(update, context):
        custom_keyboard = [['/add_event 1337'], ['/add_event 1111', '/add_event 2222']]
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Choose event or request a custom by '/add_event <4 numbers>'",
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
                                        first=TimeService.time_apply_tz(datetime.time(hours, minute, 5)),
                                        context=update.message.chat_id,
                                        name=str(time))

        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Added event '" + str(time) + "'",
                                 reply_markup=telegram.ReplyKeyboardRemove())

    ####################################################################################

    @staticmethod
    def remove_event(update, context):
        keyboard = EventService.rmv_event_keyboard(context.job_queue)
        if len(keyboard) == 0:
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text="There are no active events")
            return

        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Choose one of the following:",
                                 reply_markup=InlineKeyboardMarkup(keyboard))

    @staticmethod
    def rmv_event_callback(update, context):
        if update.callback_query.data == "rmv_event_all":
            EventService.remove_all_jobs(context.job_queue)
            update.callback_query.message.edit_text(text="All events removed.")
        elif "rmv_event" in update.callback_query.data:
            event_name = update.callback_query.data.split(" ")[1]
            EventService.remove_job(context.job_queue, event_name)
            keyboard = EventService.rmv_event_keyboard(context.job_queue)
            update.callback_query.message.edit_text(text="Removed event: " + event_name,
                                                    reply_markup=InlineKeyboardMarkup(keyboard))

    ####################################################################################

    @staticmethod
    def events(update, context):
        active_jobs = EventService.active_jobs(context.job_queue)
        if len(active_jobs) == 0:
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text="There are no active events")
            return

        reply = "*This events are active:*\n\n"
        for job in active_jobs:
            reply += "Event @ " + job.name + "\n"
        reply += "\nSever restart will reset all events."

        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=reply, parse_mode=telegram.ParseMode.MARKDOWN)
