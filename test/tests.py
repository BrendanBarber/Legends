import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../application')))

from application.core import Note
from application.utils import Location, Timerange, Description, LegendsImage

def test_location():
    location = Location(1, 2, 3)
    assert location.x == 1
    assert location.y == 2
    assert location.z == 3

    location1 = Location(-5, 0, 10000000)
    assert location1.x == -5
    assert location1.y == 0
    assert location1.z == 10000000

    locationA = Location(0, 0, 0)
    locationB = Location(5,0,0)

    assert locationA.distance_to(locationA) == 0
    assert locationA.distance_to(locationB) == 5

    locationC = Location(0, 0, 0)
    locationD = Location(-4, -3, 0)

    assert locationD.distance_to(locationC) == 5

def test_note_init():
    pass