from entity.event import Event

from typing import List


class EventRepo:

    @staticmethod
    def create(event: Event):
        event.save(force_insert=True)

    @staticmethod
    def save(event: Event):
        event.save()

    @staticmethod
    def delete(time: int):
        Event.delete().where(Event.time == time).execute()

    @staticmethod
    def exists(time: int) -> bool:
        query = Event.select().where(Event.time == time)
        return query.exists()

    @staticmethod
    def delete_all():
        all_events = EventRepo.findAll()
        for event in all_events:
            event.delete_instance()

    @staticmethod
    def findAll() -> List[Event]:
        return list(Event.select())
