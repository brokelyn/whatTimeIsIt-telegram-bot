import datetime
from typing import List

from src.entity.event import Event


class EventService:

    @staticmethod
    def triggered_by_text(events: List[Event], text: str) -> List[Event]:
        triggered = []
        for event in events:
            if str(event.trigger) in text:
                triggered.append(event)

        return triggered

    @staticmethod
    def triggered_by_time(events: List[Event], timestamp: int) -> List[Event]:
        triggered = []
        clock_time = datetime.fromtimestamp(timestamp).strftime('%H%M')
        for event in events:
            if event.trigger == clock_time:
                triggered.append(event)

        return triggered
