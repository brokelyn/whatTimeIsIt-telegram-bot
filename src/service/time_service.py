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
    def datetime_correct_tz(time: datetime) -> datetime:
        ts = time.timestamp()
        tz = pytz.timezone("Europe/Berlin")
        utc_time_off = tz.localize(datetime.utcfromtimestamp(ts))

        german_time = utc_time_off + utc_time_off.utcoffset()
        return german_time.replace(tzinfo=None)  # remove offset

    @staticmethod
    def datetime_apply_tz(time: datetime) -> datetime:
        tz = pytz.timezone("Europe/Berlin")
        time_off = tz.localize(time)

        return time_off
