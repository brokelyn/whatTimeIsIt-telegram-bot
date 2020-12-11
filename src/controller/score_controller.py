
class ScoreController:

    @staticmethod
    def score(update, context):
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Not supported yet")
