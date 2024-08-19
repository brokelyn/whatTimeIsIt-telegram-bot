import telegram

import service.util_service as UtilService
from service.time_service import TimeService
import service.event_service as EventService


class EventController:

    @staticmethod
    async def add_event(update, context):
        if UtilService.is_private_chat(update.message, context.bot):
            return

        if len(context.args) <= 0:
            await EventController.add_keyboard(update, context)
        else:
            time = TimeService.is_valid_time(context.args[0])
            if time != -1:
                await EventController.add_job(update, context, time)
            else:
                await context.bot.send_message(chat_id=update.message.chat.id,
                                         text="Time request is invalid")

    @staticmethod
    async def add_keyboard(update, context):
        custom_keyboard = [['/add_event 1337', '/add_event 0'], ['/add_event 1111', '/add_event 2222']]
        await context.bot.send_message(chat_id=update.message.chat.id,
                                 text="Choose event or request a custom by '/add_event <4 numbers>'",
                                 reply_markup=telegram.ReplyKeyboardMarkup(custom_keyboard))

    @staticmethod
    async def add_job(update, context, time: int):
        if EventService.is_event_already_active(context.job_queue, update.message.chat.id, time):
            await context.bot.send_message(chat_id=update.message.chat.id,
                                     text="The event " + str(time) + " already exists",
                                     reply_markup=telegram.ReplyKeyboardRemove())
        else:
            EventService.create_event(context.job_queue, update.message.chat.id, time)

            await context.bot.send_message(chat_id=update.message.chat.id,
                                     text="Added event '" + str(time) + "'",
                                     reply_markup=telegram.ReplyKeyboardRemove())

    ####################################################################################

    @staticmethod
    async def remove_event(update, context):
        if UtilService.is_private_chat(update.message, context.bot):
            return

        keyboard = EventService.rmv_event_keyboard(context.job_queue, update.message.chat.id)
        if len(keyboard) == 0:
            await context.bot.send_message(chat_id=update.message.chat.id,
                                     text="There are no active events")
        else:
            await context.bot.send_message(chat_id=update.message.chat.id,
                                     text="Choose one of the following:",
                                     reply_markup=telegram.InlineKeyboardMarkup(keyboard))

    @staticmethod
    async def rmv_event_callback(update, context):
        group_id = update.callback_query.message.chat.id

        if update.callback_query.data == "rmv_event_all":
            EventService.remove_all_group_events(context.job_queue, group_id)
            await update.callback_query.message.edit_text(text="All events removed.")
        elif "rmv_event" in update.callback_query.data:
            event_name = update.callback_query.data.split(" ")[1]
            EventService.remove_group_event(context.job_queue, group_id, event_name)
            keyboard = EventService.rmv_event_keyboard(context.job_queue, group_id)

            text = "Removed event: " + event_name
            if len(keyboard) == 0:
                text += '\n\nNo more events left!'

            await update.callback_query.message.edit_text(text=text,
                                                    reply_markup=telegram.InlineKeyboardMarkup(keyboard))

    ####################################################################################

    @staticmethod
    async def events(update, context):
        if UtilService.is_private_chat(update.message, context.bot):
            return

        active_jobs = EventService.list_active_jobs(context.job_queue, update.message.chat.id)
        if len(active_jobs) == 0:
            await context.bot.send_message(chat_id=update.message.chat.id, text="There are no active events")
        else:
            reply = "*This events are active:*\n\n"
            for job in active_jobs:
                job_time = job.name.split("/")[0]
                reply += "Event @ " + job_time + "\n"

            await context.bot.send_message(chat_id=update.message.chat.id,
                                     text=reply, parse_mode=telegram.constants.ParseMode.MARKDOWN)
