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
    def datetime_apply_tz(time: datetime, exclude_off=True) -> datetime:
        ts = time.timestamp()
        tz = pytz.timezone("Europe/Berlin")
        utc_time_off = tz.localize(datetime.utcfromtimestamp(ts))

        if exclude_off:
            german_time = utc_time_off + utc_time_off.utcoffset()
            return german_time.replace(tzinfo=None)  # remove offset
        else:
            return utc_time_off
