import telegram
from telegram import InlineKeyboardMarkup

from service.time_service import TimeService
from service.event_service import EventService
from repo.event_repo import EventRepo



class EventController:

    @staticmethod
    def add_event(update, context):
        if len(context.args) <= 0:
            EventController.add_keyboard(update, context)
        else:
            time = TimeService.is_valid_time(context.args[0])
            if time is not -1:
                EventController.add_job(update, context, time)
            else:
                context.bot.send_message(chat_id=update.message.chat_id,
                                         text="Time request is invalid")

    @staticmethod
    def add_keyboard(update, context):
        custom_keyboard = [['/add_event 1337', '/add_event 0'], ['/add_event 1111', '/add_event 2222']]
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Choose event or request a custom by '/add_event <4 numbers>'",
                                 reply_markup=telegram.ReplyKeyboardMarkup(custom_keyboard))

    @staticmethod
    def add_job(update, context, time: int):
        if len(context.job_queue.get_jobs_by_name(str(time))) > 0 or EventRepo.exists(time):
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text="This event already exists",
                                     reply_markup=telegram.ReplyKeyboardRemove())
            return

        EventService.create_event(context.job_queue, update.message.chat_id, time)

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
            EventService.remove_all_events(context.job_queue)
            update.callback_query.message.edit_text(text="All events removed.")
        elif "rmv_event" in update.callback_query.data:
            event_name = update.callback_query.data.split(" ")[1]
            EventService.remove_event(context.job_queue, event_name)
            keyboard = EventService.rmv_event_keyboard(context.job_queue)
            update.callback_query.message.edit_text(text="Removed event: " + event_name,
                                                    reply_markup=InlineKeyboardMarkup(keyboard))

    ####################################################################################

    @staticmethod
    def events(update, context):
        active_jobs = EventService.active_jobs(context.job_queue)
        if len(active_jobs) == 0:
            context.bot.send_message(chat_id=update.message.chat_id, text="There are no active events")
        else:
            reply = "*This events are active:*\n\n"
            for job in active_jobs:
                reply += "Event @ " + job.name + "\n"

            context.bot.send_message(chat_id=update.message.chat_id,
                                     text=reply, parse_mode=telegram.ParseMode.MARKDOWN)
