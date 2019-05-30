from src.entity.message import Message
from src.messenger.telegram.telegram_api import TelegramApi
from src.repo.event_repo import EventRepo
from src.service.event_service import EventService


class EventController:

    @staticmethod
    def create_event(msg: Message):
        TelegramApi.send_msg(msg.chat_id, "'/createEvent' is currently not supported")

    @staticmethod
    def remove_event(msg: Message):
        TelegramApi.send_msg(msg.chat_id, "'/removeEvent' is currently not supported")

    @staticmethod
    def event_trigger(msg: Message):
        all_events = EventRepo.findAll()

        triggered = EventService.triggered_by_text(all_events, msg.text)
        triggered = EventService.triggered_by_time(triggered, msg.time)

        # todo
