class Timestamp:
    def __init__(self, day: int, month: int, year: int):
        self.day = day
        self.month = month
        self.year = year

    def time_between(self, timestamp: "Timestamp"):
        if not isinstance(timestamp, Timestamp):
            raise TypeError("Argument must be of type Timestamp.")
        # Can't really make until I set up the global "time" system for setting up the fictional calendar
        return -1

    def __repr__(self):
        return f"Timestamp(day={self.day}, month={self.month}, year={self.year})"

class Timerange:
    def __init__(self, start: Timestamp, end: Timestamp):
        self.start = start
        self.end = end
        self.length = start.time_between(end)

    def __repr__(self):
        return f"Timerange(start={repr(self.start)}, end={repr(self.end)}, length={self.length})"