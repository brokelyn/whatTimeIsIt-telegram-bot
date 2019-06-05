import logging

import telegram, os
from telegram.ext import CommandHandler, Updater, CallbackQueryHandler
from telegram.ext import MessageHandler, Filters

from controller.event_controller import EventController
from controller.statistic_controller import StatisticController
from controller.util_controller import UtilController

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

class BotController:

    def __init__(self):
        updater = Updater(token=os.environ['BOT_API_KEY'], use_context=True)  # used in version 12
        dispatcher = updater.dispatcher

        stat_handler = CommandHandler('stats', StatisticController.stats)
        dispatcher.add_handler(stat_handler)

        help_handler = CommandHandler('help', BotController.help)
        dispatcher.add_handler(help_handler)

        event_handler = CommandHandler('events', EventController.events)
        dispatcher.add_handler(event_handler)

        add_event_handler = CommandHandler('add_event', EventController.add_event)
        dispatcher.add_handler(add_event_handler)

        remove_event_handler = CommandHandler('remove_event', EventController.remove_event)
        dispatcher.add_handler(remove_event_handler)

        callback_rmv_event = CallbackQueryHandler(EventController.rmv_event_callback,
                                                  pattern='rmv_event')
        dispatcher.add_handler(callback_rmv_event)

        time_req_handler = CommandHandler('time', UtilController.message_time)
        dispatcher.add_handler(time_req_handler)

        message_handler = MessageHandler(Filters.text, UtilController.handle_text_msg)
        dispatcher.add_handler(message_handler)

        # needs to be the last handler
        unknown_handler = MessageHandler(Filters.command, BotController.unknown)
        dispatcher.add_handler(unknown_handler)

        print("Bot ready for requests")

        updater.start_polling()
        updater.idle()

    @staticmethod
    def unknown(update, context):
        update.message.reply_text("Unknown command")

    @staticmethod
    def help(update, context):
        help_page = "*WhatTimeIsIt Bot Help Page*\n\n"
        help_page += "-'/help' to show this help\n"
        help_page += "-'/stats <time>' to show stats for time\n"
        help_page += "-'/events' to show all daily posted stats\n"
		help_page += "-'/time' and repley a message to see its timestamp\n"
        help_page += "-'/add_event <time>' to add an event at time\n"
        help_page += "-'/remove_event' to remove a active event\n\n"
        help_page += "All text messages will be saved for analysing the scores. By participating"
        help_page += "in this group you accept this condition.\n\n"
        help_page += "Check out the [Telegram Bot](https://github.com/python-telegram-bot/python-telegram-bot) framework"

        context.bot.send_message(chat_id=update.message.chat_id, text=help_page,
                                 reply_markup=telegram.ReplyKeyboardRemove(),
                                 parse_mode=telegram.ParseMode.MARKDOWN)
