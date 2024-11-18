from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict
import json

@dataclass
class TimeUnit:
    name: str                      # Name of this unit (e.g., "Month", "Day")
    number: int                    # Default number of this unit to make up 1 parent unit (optional for variability)
    parent: Optional[TimeUnit] = None  # Parent unit in the hierarchy
    child: Optional[TimeUnit] = None   # Child unit in the hierarchy (default: None)
    names: List[str] = field(default_factory=list)  # Optional names for instances of this unit (e.g., names of months)
    custom_lengths: Dict[str, int] = field(default_factory=dict)  # Specific lengths for named instances (e.g., {"February": 28, "February Leap": 29})

    def add_child(self, child: TimeUnit):
        """Sets the child TimeUnit, establishing the relationship."""
        self.child = child
        child.parent = self

    def get_length(self, name: Optional[str] = None) -> int:
        """Gets the length of this unit based on the name, or defaults."""
        if name and name in self.custom_lengths:
            return self.custom_lengths[name]
        return self.number

    def total_length(self) -> int:
        """Calculates the total length of this unit, factoring in child units."""
        if self.child:
            return self.number * self.child.total_length()
        return self.number

    def to_dict(self) -> dict:
        """Convert the TimeUnit to a dictionary."""
        return {
            "name": self.name,
            "number": self.number,
            "names": self.names,
            "custom_lengths": self.custom_lengths,
            "child": self.child.to_dict() if self.child else None
        }

    @staticmethod
    def from_dict(data: dict) -> 'TimeUnit':
        """Reconstruct a TimeUnit from a dictionary."""
        unit = TimeUnit(
            name=data["name"],
            number=data["number"],
            names=data.get("names", []),
            custom_lengths=data.get("custom_lengths", {})
        )
        if data.get("child"):
            unit.child = TimeUnit.from_dict(data["child"])
            unit.child.parent = unit  # Restore the parent reference
        return unit

    # Returns json string
    def serialize(self) -> str:
        """Serialize object to a JSON string"""
        return json.dumps(self.to_dict())

    @staticmethod
    def deserialize(data: str) -> 'TimeUnit':
        """Deserialize a JSON string into a TimeUnit."""
        return TimeUnit.from_dict(json.loads(data))

@dataclass
class Calendar:
    time_unit_list: TimeUnit       # Root of the TimeUnit LinkedList
    leap_day_freq: int = 4         # Frequency of leap years
    leap_day_amount: int = 1       # Number of leap days to add
    leap_unit: Optional[TimeUnit] = None  # Unit to which leap day(s) are added (e.g., days)

    def get_unit_hierarchy(self) -> List[Dict[str, str]]:
        """Returns a structured view of the hierarchy for debugging or display."""
        units = []
        current = self.time_unit_list
        while current:
            units.append({"name": current.name, "number": current.number, "child": current.child.name if current.child else None})
            current = current.child
        return units

    def calculate_leap_year_adjustment(self, year: int) -> int:
        """Returns the additional days for a given year if it's a leap year."""
        if self.leap_day_freq and year % self.leap_day_freq == 0:
            return self.leap_day_amount
        return 0

    def to_dict(self) -> dict:
        """Convert the Calendar to a dictionary."""
        return {
            "time_unit_list": self.time_unit_list.to_dict(),
            "leap_day_freq": self.leap_day_freq,
            "leap_day_amount": self.leap_day_amount,
            "leap_unit": self.leap_unit.name if self.leap_unit else None
        }

    @staticmethod
    def from_dict(data: dict) -> 'Calendar':
        """Reconstruct a Calendar from a dictionary."""
        root_unit = TimeUnit.from_dict(data["time_unit_list"])
        calendar = Calendar(
            time_unit_list=root_unit,
            leap_day_freq=data.get("leap_day_freq", 4),
            leap_day_amount=data.get("leap_day_amount", 1),
            leap_unit=None
        )
        # Restore leap_unit if it exists
        if data.get("leap_unit"):
            current = root_unit
            while current:
                if current.name == data["leap_unit"]:
                    calendar.leap_unit = current
                    break
                current = current.child
        return calendar

    def serialize(self) -> str:
        """Serialize the Calendar to a JSON string."""
        return json.dumps(self.to_dict())

    @staticmethod
    def deserialize(data: str) -> 'Calendar':
        """Deserialize a JSON string into a Calendar."""
        return Calendar.from_dict(json.loads(data))

def default_calendar() -> Calendar:
    # Define time units
    seconds = TimeUnit(name="Second", number=60)
    minutes = TimeUnit(name="Minute", number=60)
    hours = TimeUnit(name="Hour", number=24)
    days = TimeUnit(name="Day", number=30)
    months = TimeUnit(
        name="Month",
        number=12,
        names=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
               "November", "December"],
        custom_lengths={
            "January": 31,
            "February": 28,
            "February Leap": 29,
            "March": 31,
            "April": 30,
            "May": 31,
            "June": 30,
            "July": 31,
            "August": 31,
            "September": 30,
            "October": 31,
            "November": 30,
            "December": 31
        }
    )

    # Link the units
    seconds.add_child(minutes)
    minutes.add_child(hours)
    hours.add_child(days)
    days.add_child(months)

    # Create a calendar
    return Calendar(
        time_unit_list=seconds,
        leap_day_freq=4,    # Every 4 years
        leap_day_amount=1,
        leap_unit=days      # Leap day(s) added to the "Day" unit
    )

def stormlight_calendar() -> Calendar:
    # Define the smallest unit
    seconds = TimeUnit(name="Second", number=60, parent=None)
    minutes = TimeUnit(name="Minute", number=60, parent=seconds)
    hours = TimeUnit(name="Hour", number=24, parent=minutes)
    days = TimeUnit(name="Day", number=5, parent=hours)  # Week has 5 days
    weeks = TimeUnit(name="Week", number=10, parent=days)  # Month has 10 weeks
    months = TimeUnit(
        name="Month",
        number=10,  # 10 months per year
        parent=weeks,
        names=[
            "Jes", "Nan", "Chach", "Vev", "Palah",
            "Shash", "Betab", "Kak", "Tanat", "Ishi"
        ],
        custom_lengths={month: 50 for month in [
            "Jes", "Nan", "Chach", "Vev", "Palah",
            "Shash", "Betab", "Kak", "Tanat", "Ishi"
        ]}
    )
    years = TimeUnit(name="Year", number=10, parent=months)  # 1 year = 10 months

    # Link the units
    seconds.add_child(minutes)
    minutes.add_child(hours)
    hours.add_child(days)
    days.add_child(weeks)
    weeks.add_child(months)
    months.add_child(years)

    # Create the calendar
    return Calendar(
        time_unit_list=seconds,
        leap_day_freq=0,     # No leap years
        leap_day_amount=0,   # No additional leap days
        leap_unit=None       # No leap days
    )

class Settings:
    def __init__(self, calendar: Calendar):
        self.calendar = calendar

    def to_dict(self) -> dict:
        """Convert Settings to a dictionary."""
        return {
            "calendar": self.calendar
        }

    @staticmethod
    def from_dict(data: dict) -> 'Settings':
        """Reconstruct Settings from a dictionary."""
        return Settings(
            calendar=Calendar.from_dict(data)
        )

    def serialize(self) -> str:
        """Serialize the Calendar to a JSON string."""
        return json.dumps(self.to_dict())

    @staticmethod
    def deserialize(data: str) -> 'Settings':
        """Deserialize a JSON string into a Calendar."""
        return Settings.from_dict(json.loads(data))