import dateutil.tz
from datetime import datetime

class TimeService:

    @staticmethod
    def is_valid_time(time_str: str) -> [bool, str]:
        try:
            time = int(time_str)
        except ValueError:
            return [False, "No valid time"]
        if time > 2359:
            return [False, "Time too big"]
        elif time < 0:
            return [False, "Time too small"]
        else:
            return [True, "Valid time"]

    @staticmethod
    def parse_to_tz(time: datetime) -> datetime:
        # offset +2 hours for german time
        return time.replace(tzinfo=dateutil.tz.tzoffset(None, 2 * (60 * 60)))
