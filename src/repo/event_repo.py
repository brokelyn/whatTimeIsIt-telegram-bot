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
    def delete(group_id: int, time: int):
        query = Event.delete().where(Event.group == group_id, Event.time == time)
        if query.execute() == 0:
            raise ReferenceError("Could not find object to delete: GroupId: " + group_id + ", Time: " + time)


    @staticmethod
    def exists(group_id: int, time: int) -> bool:
        query = Event.select().where(Event.time == time, Event.group == group_id)
        return query.exists()

    @staticmethod
    def delete_all_for_group(group_id: int):
        Event.delete().where(Event.group == group_id).execute()

    @staticmethod
    def findAll() -> List[Event]:
        return list(Event.select())
