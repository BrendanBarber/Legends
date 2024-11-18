import json
from typing import List, Optional
from application.utils import Location, Timerange, Description, LegendsImage

class Tag:
    def __init__(self, id: int, name: str, color: int):
        self.id = id
        self.name = name
        self.color = color

class Note:
    def __init__(self,
                 id: int,
                 location: Location,
                 timerange: Timerange,
                 description: Description,
                 thumbnail: LegendsImage,
                 attached_images: Optional[List[LegendsImage]] = None,
                 parent: Optional['Note'] = None,
                 children: Optional[List['Note']] = None,
                 tags: Optional[List['Tag']] = None):
        self.id = id
        self.location = location
        self.timerange = timerange
        self.description = description
        self.thumbnail = thumbnail

        self.attached_images = attached_images if attached_images is not None else []
        if not all(isinstance(image, LegendsImage) for image in self.attached_images):
            raise TypeError("Each attached image must be a LegendsImage.")

        self.parent = parent
        if self.parent is not None and not isinstance(self.parent, Note):
            raise TypeError("Parent must be a Note.")

        self.children = children if children is not None else []
        if not all(isinstance(child, Note) for child in self.children):
            raise TypeError("Each child must be a Note.")

        self.tags = tags if tags is not None else []
        if not all(isinstance(tag, Tag) for tag in self.tags):
            raise TypeError("Each tag must be a Tag.")

    def attach_image(self, image: LegendsImage):
        self.attached_images.append(image)

    def __repr__(self):
        return (f"Note(location={repr(self.location)}, timerange={repr(self.timerange)}, "
                f"description={repr(self.description)}, thumbnail={repr(self.thumbnail)}, "
                f"attached_images={len(self.attached_images)} images)")

    def to_dict(self) -> dict:
        """Convert the Note to a dictionary."""
        return {
            "id": self.id,
            "location": self.location.to_dict() if hasattr(self.location, "to_dict") else str(self.location),
            "timerange": self.timerange.to_dict() if hasattr(self.timerange, "to_dict") else str(self.timerange),
            "description": self.description.to_dict() if hasattr(self.description, "to_dict") else str(self.description),
            "thumbnail": self.thumbnail.to_dict() if hasattr(self.thumbnail, "to_dict") else str(self.thumbnail),
            "attached_images": [img.to_dict() if hasattr(img, "to_dict") else str(img) for img in self.attached_images],
            "parent_id": self.parent.id if self.parent else None,
            "children": [child.to_dict() for child in self.children]
        }

    @staticmethod
    def from_dict(data: dict, note_registry: Optional[dict] = None) -> 'Note':
        """Reconstruct a Note from a dictionary."""
        note_registry = note_registry or {}

        note = Note(
            id=data["id"],
            location=Location.from_dict(data["location"]) if hasattr(Location, "from_dict") else Location(
                data["location"]),
            timerange=Timerange.from_dict(data["timerange"]) if hasattr(Timerange, "from_dict") else Timerange(
                data["timerange"]),
            description=Description.from_dict(data["description"]) if hasattr(Description,
                                                                              "from_dict") else Description(
                data["description"]),
            thumbnail=LegendsImage.from_dict(data["thumbnail"]) if hasattr(LegendsImage, "from_dict") else LegendsImage(
                data["thumbnail"]),
            attached_images=[
                LegendsImage.from_dict(img) if hasattr(LegendsImage, "from_dict") else LegendsImage(img)
                for img in data.get("attached_images", [])
            ],
            parent=None,  # Will be linked later
            children=[]  # Will be populated later
        )

        note_registry[note.id] = note

        # Link children recursively
        for child_data in data.get("children", []):
            child_note = Note.from_dict(child_data, note_registry)
            note.children.append(child_note)
            child_note.parent = note

        return note

    def serialize(self) -> str:
        """Serialize the Note to a JSON string."""
        return json.dumps(self.to_dict())

    @staticmethod
    def deserialize(data: str) -> 'Note':
        """Deserialize a JSON string into a Note."""
        return Note.from_dict(json.loads(data))