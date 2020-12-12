import telegram
from telegram import InlineKeyboardMarkup

from service.time_service import TimeService
from service.event_service import EventService


class EventController:

    @staticmethod
    def add_event(update, context):
        if len(context.args) <= 0:
            EventController.add_keyboard(update, context)
        else:
            time = TimeService.is_valid_time(context.args[0])
            if time != -1:
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
        if EventService.is_event_already_active(update, context, time):
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text="The event " + str(time) + " already exists",
                                     reply_markup=telegram.ReplyKeyboardRemove())
        else:
            EventService.create_event(context.job_queue, update.message.chat_id, time)

            context.bot.send_message(chat_id=update.message.chat_id,
                                     text="Added event '" + str(time) + "'",
                                     reply_markup=telegram.ReplyKeyboardRemove())

    ####################################################################################

    @staticmethod
    def remove_event(update, context):
        keyboard = EventService.rmv_event_keyboard(context.job_queue, update.message.chat_id)
        if len(keyboard) == 0:
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text="There are no active events")
        else:
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text="Choose one of the following:",
                                     reply_markup=InlineKeyboardMarkup(keyboard))

    @staticmethod
    def rmv_event_callback(update, context):
        group_id = update.callback_query.message.chat.id

        if update.callback_query.data == "rmv_event_all":
            EventService.remove_all_group_events(context.job_queue, group_id)
            update.callback_query.message.edit_text(text="All events removed.")
        elif "rmv_event" in update.callback_query.data:
            event_name = update.callback_query.data.split(" ")[1]
            EventService.remove_group_event(context.job_queue, group_id, event_name)
            keyboard = EventService.rmv_event_keyboard(context.job_queue, group_id)

            text = "Removed event: " + event_name
            if len(keyboard) == 0:
                text += '\n\nNo more events left!'

            update.callback_query.message.edit_text(text=text,
                                                    reply_markup=InlineKeyboardMarkup(keyboard))

    ####################################################################################

    @staticmethod
    def events(update, context):
        active_jobs = EventService.active_jobs(context.job_queue, update.message.chat_id)
        if len(active_jobs) == 0:
            context.bot.send_message(chat_id=update.message.chat_id, text="There are no active events")
        else:
            reply = "*This events are active:*\n\n"
            for job in active_jobs:
                job_time = job.name.split("/")[0]
                reply += "Event @ " + job_time + "\n"

            context.bot.send_message(chat_id=update.message.chat_id,
                                     text=reply, parse_mode=telegram.ParseMode.MARKDOWN)
