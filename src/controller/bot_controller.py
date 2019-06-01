import telegram
from telegram.ext import CommandHandler, Updater
from telegram.ext import MessageHandler, Filters

from src.controller.statistic_controller import StatisticController
from src.controller.event_controller import EventController
from src.controller.base_controller import persist_message


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

        remove_all_events_handler = CommandHandler('removeAllEvents', EventController.remove_all_jobs)
        dispatcher.add_handler(remove_all_events_handler)

        message_handler = MessageHandler(Filters.text, persist_message)
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
    def help(update, context):  # todo html correct parsing
        help_page = "<b> This is the Help </b>\n" \
                    "- '/help' to show this help\n" \
                    "- '/stats <time>' to show stats for time\n" \
                    "- '/events' to show all daily posted stats\n" \
                    "- '/addEvent <time>' to add an event at time\n" \
                    "- '/removeEvent <time>' to remove the event at time\n" \
                    "- '/removeAllEvents' to remove all active events\n" \
                    "\n All text messages will be saved for analysing the scores. By participating" \
                    "in this group you accept this condition."

        context.bot.send_message(chat_id=update.message.chat_id, text=help_page,
                                 reply_markup=telegram.ReplyKeyboardRemove())  # ,
        # parse_mode=telegram.ParseMode.HTML)
