from datetime import datetime, timedelta, time

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
    def datetime_apply_tz(time: datetime) -> datetime:
        # offset +2 hours for german time
        ts = time.timestamp()
        german_time = datetime.utcfromtimestamp(ts) + timedelta(hours=2)
        return german_time

    @staticmethod
    def time_apply_tz(ts: time) -> time:
        print(str(ts))
        if TimeService.is_utc_time():
            print("Corrected time: " + str(time((ts.hour + 2) % 24, ts.minute, ts.second)))
            return time((ts.hour + 2) % 24, ts.minute, ts.second)
        return ts

    @staticmethod
    def is_utc_time() -> bool:
        local_time = datetime.now()
        utc_ts = local_time.timestamp()
        utc = datetime.utcfromtimestamp(utc_ts).strftime("%H%M %d%m%Y")
        print("Utc time: " + str(utc))
        local = local_time.strftime("%H%M %d%m%Y")
        print("Loc time " + str(local))
        if utc is local:
            return True
        return False
