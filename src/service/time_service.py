from datetime import datetime
from datetime import timedelta
import pytz


class TimeService:

    @staticmethod
    def timedelta_until_next_day() -> timedelta:
        dt = datetime.now()
        dt_tomorrow = dt.replace(hour=0, minute=0, second=0)
        dt_tomorrow = dt_tomorrow + timedelta(days=1)

        return dt_tomorrow - dt

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
    def datetime_correct_tz(time: datetime, timezone: str) -> datetime:
        tz = pytz.timezone(timezone)
        utc_time_off = tz.localize(time.replace(tzinfo=None))

        game_time = utc_time_off + utc_time_off.utcoffset()
        return game_time.replace(tzinfo=None)  # remove offset

    @staticmethod
    def datetime_apply_tz(time: datetime, timezone: str) -> datetime:
        tz = pytz.timezone(timezone)
        time_off = tz.localize(time)

        return time_off
