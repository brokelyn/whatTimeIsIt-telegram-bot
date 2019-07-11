from datetime import datetime, timedelta, time

class TimeService:

    @staticmethod
    def is_valid_time(time_str: str) -> int:
        try:
            time = int(time_str)
        except ValueError:
            return -1
        if 0 > time > 2359:
            return -1
        if len(time_str) > 2 and int(time_str[-2]) > 5:
            return -1
        else:
            return time

    @staticmethod
    def datetime_apply_tz(time: datetime) -> datetime:
        # offset +2 hours for german time
        ts = time.timestamp()
        german_time = datetime.utcfromtimestamp(ts) + timedelta(hours=2)
        return german_time

    @staticmethod
    def time_apply_tz(ts: time) -> time:
        if TimeService.is_utc_time():
            return time((ts.hour - 2) % 24, ts.minute, ts.second)
        return ts

    @staticmethod
    def is_utc_time() -> bool:
        local_time = datetime.now()
        utc_ts = local_time.timestamp()
        utc = datetime.utcfromtimestamp(utc_ts).strftime("%Y%m%d%H%M")
        local = local_time.strftime("%Y%m%d%H%M")
        if int(utc) == int(local):
            return True
        return False
