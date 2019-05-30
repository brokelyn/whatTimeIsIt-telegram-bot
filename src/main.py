import src.database
from src.controller.main_controller import MainController

src.database.init()

main_controller = MainController()

main_controller.start_listening(timeout=3)
