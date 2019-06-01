import src.database
from src.controller.bot_controller import BotController

src.database.init()

main_controller = BotController()
