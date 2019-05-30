from typing import List

from src.entity.event import Event


class EventRepo:

    @staticmethod
    def save(event: Event):
        event.save()

    @staticmethod
    def findAll() -> List[Event]:
        query = Event.select()
        return list(query)
