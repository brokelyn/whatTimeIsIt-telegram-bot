from datetime import datetime, time
import pytz

class TimeService:

    @staticmethod
    def is_valid_time(time_str: str, modulo=True) -> int:
        # -1         , invalid
        # time as int, valid
        try:
            time = int(time_str)
        except ValueError:
            return -1
        if modulo:
            if len(time_str) > 4 or time < 0:
                return -1
            minutes = time % 100
            hours = int((time - minutes) / 100)
            if minutes > 59:
                hours = hours + 1
                minutes = minutes - 60
            hours = hours % 24
            time = 100 * hours + minutes
            return time
        else:
            if 0 > time or time > 2359:
                return -1
            if len(time_str) > 2 and int(time_str[-2]) > 5:
                return -1
            return time

    @staticmethod
    def datetime_correct_tz(time: datetime) -> datetime:
        ts = time.timestamp()
        tz = pytz.timezone("Europe/Berlin")
        utc_time_off = tz.localize(datetime.utcfromtimestamp(ts))

        gamezone_time = utc_time_off + utc_time_off.utcoffset()
        return gamezone_time.replace(tzinfo=None)  # remove offset

    @staticmethod
    def datetime_apply_tz(time: datetime) -> datetime:
        tz = pytz.timezone("Europe/Berlin")
        time_off = tz.localize(time)

        return time_off
