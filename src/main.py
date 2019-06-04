import database
from src.controller.bot_controller import BotController

database.init()

main_controller = BotController()
