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
