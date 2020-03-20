from datetime import datetime, time
import pytz

class TimeService:

    @staticmethod
    def is_valid_time(time_str: str) -> int:
        # -1         , invalid
        # time as int, valid
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
        ts = time.timestamp()
        tz = pytz.timezone("Europe/Berlin")
        german_time_off = tz.localize(datetime.utcfromtimestamp(ts))
        german_time = german_time_off + german_time_off.utcoffset()
        return german_time.replace(tzinfo=None)  # remove offset

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
