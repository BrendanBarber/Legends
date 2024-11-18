import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../application')))

from application.core import Note
from application.utils import Location, Timestamp, Timerange, Description, LegendsImage

def test_notes():
    location = Location(0, 0, 0)

    start = Timestamp(1, 1, 0)
    end = Timestamp(1, 6, 10)

    timerange = Timerange(start, end)

    description = Description("*This is a **note**.*")

    legends_image = None

    note1 = Note(location, timerange, description, legends_image, legends_image, None, None)