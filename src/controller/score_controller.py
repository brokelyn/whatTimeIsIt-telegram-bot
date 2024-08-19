
class ScoreController:

    @staticmethod
    async def score(update, context):
        await context.bot.send_message(chat_id=update.message.chat.id,
                                 text="Not supported yet")
