from src.entity.bot import Bot


class BotRepo:

    @staticmethod
    def findByName(botname: str) -> Bot:
        return Bot.get(name=botname)

    @staticmethod
    def save(bot: Bot):
        bot.save()
