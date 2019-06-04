import telegram
from telegram.ext import CommandHandler, Updater, CallbackQueryHandler
from telegram.ext import MessageHandler, Filters

from src.controller.event_controller import EventController
from src.controller.statistic_controller import StatisticController
from src.controller.base_controller import handle_text_msg


class BotController:

    def __init__(self):
        bot_token = "836568720:AAHCvDJ3qLaausxazb5BVlWfKIBsaVadIZc"
        updater = Updater(token=bot_token, use_context=True)
        dispatcher = updater.dispatcher

        stat_handler = CommandHandler('stats', StatisticController.stats)
        dispatcher.add_handler(stat_handler)

        help_handler = CommandHandler('help', BotController.help)
        dispatcher.add_handler(help_handler)

        event_handler = CommandHandler('events', EventController.events)
        dispatcher.add_handler(event_handler)

        add_event_handler = CommandHandler('addEvent', EventController.add_event)
        dispatcher.add_handler(add_event_handler)

        remove_event_handler = CommandHandler('removeEvent', EventController.remove_event)
        dispatcher.add_handler(remove_event_handler)

        callback_rmv_event = CallbackQueryHandler(EventController.rmv_event_callback,
                                                  pattern='rmv_event')
        dispatcher.add_handler(callback_rmv_event)

        message_handler = MessageHandler(Filters.text, handle_text_msg)
        dispatcher.add_handler(message_handler)

        # needs to be the last handler
        unknown_handler = MessageHandler(Filters.command, BotController.unknown)
        dispatcher.add_handler(unknown_handler)

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
        help_page += "-'/addEvent <time>' to add an event at time\n"
        help_page += "-'/removeEvent' to remove a active event\n\n"
        help_page += "All text messages will be saved for analysing the scores. By participating"
        help_page += "in this group you accept this condition.\n\n"
        help_page += "Check out the [Telegram Bot](https://github.com/python-telegram-bot/python-telegram-bot) framework"

        context.bot.send_message(chat_id=update.message.chat_id, text=help_page,
                                 reply_markup=telegram.ReplyKeyboardRemove(),
                                 parse_mode=telegram.ParseMode.MARKDOWN)