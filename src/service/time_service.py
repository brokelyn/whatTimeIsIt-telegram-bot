from datetime import datetime, timedelta

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
        ts = time.timestamp()
        german_time = datetime.utcfromtimestamp(ts) + timedelta(hours=2)
        return german_time
