from src.entity.event import Event


class EventRepo:

    @staticmethod
    def save(event: Event):
        event.save()
