from typing import List, Dict
from settings import Settings
from map import MapElement, MapImageElement, MapAzgaarElement
from note import Note

# Project
    # ID
    # Name
    # Settings
    # Many MapElements
    # Many Notes

class Project:
    def __init__(self, id: int, name: str, settings: Settings, map_elements: Dict[int, MapElement], notes: Dict[int, Note]):
        self.id = id
        self.name = name
        self.settings = settings
        self.map_elements = map_elements
        self.notes = notes

    # To JSON
    def serialize(self):
        pass

    # To File
    def save(self):
        pass

# From File
def load_project(file_path: str):
    pass