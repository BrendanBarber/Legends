from application.utils import Location, Scale, LegendsImage
import json

class MapElement:
    def __init__(self, id: int, location: 'Location', scale: 'Scale', rotation: float):
        self.id = id
        self.location = location
        self.scale = scale
        self.rotation = rotation

    def to_dict(self) -> dict:
        """Serialize the MapElement to a dictionary."""
        return {
            "id": self.id,
            "location": self.location.to_dict() if hasattr(self.location, "to_dict") else str(self.location),
            "scale": self.scale.to_dict() if hasattr(self.scale, "to_dict") else str(self.scale),
            "rotation": self.rotation,
            "type": self.__class__.__name__
        }

    @staticmethod
    def from_dict(data: dict) -> 'MapElement':
        """Reconstruct a MapElement or its subclass from a dictionary."""
        element_type = data.get("type", "MapElement")
        if element_type == "MapImageElement":
            return MapImageElement.from_dict(data)
        elif element_type == "MapAzgaarElement":
            return MapAzgaarElement.from_dict(data)
        else:
            return MapElement(
                id=data["id"],
                location=Location.from_dict(data["location"]) if hasattr(Location, "from_dict") else Location(0,0,0),
                scale=Scale.from_dict(data["scale"]) if hasattr(Scale, "from_dict") else Scale(1,1,0),
                rotation=data["rotation"]
            )

    def serialize(self) -> str:
        """Serialize the MapElement to a JSON string."""
        return json.dumps(self.to_dict())

    @staticmethod
    def deserialize(data: str) -> 'MapElement':
        """Deserialize a JSON string into a MapElement or its subclass."""
        return MapElement.from_dict(json.loads(data))

class MapImageElement(MapElement):
    def __init__(self, id: int, location: 'Location', scale: 'Scale', rotation: float, image: LegendsImage):
        super().__init__(id, location, scale, rotation)
        self.image = image

    def to_dict(self) -> dict:
        """Serialize the MapImageElement to a dictionary."""
        base_dict = super().to_dict()
        base_dict.update({
            "image": self.image.to_dict() if hasattr(self.image, "to_dict") else str(self.image)
        })
        return base_dict

    @staticmethod
    def from_dict(data: dict) -> 'MapImageElement':
        """Reconstruct a MapImageElement from a dictionary."""
        return MapImageElement(
            id=data["id"],
            location=Location.from_dict(data["location"]) if hasattr(Location, "from_dict") else Location(0,0,0),
            scale=Scale.from_dict(data["scale"]) if hasattr(Scale, "from_dict") else Scale(1,1,0),
            rotation=data["rotation"],
            image=LegendsImage.from_dict(data["image"]) if hasattr(LegendsImage, "from_dict") else LegendsImage(data["image"])
        )

class MapAzgaarElement(MapElement):
    def __init__(self, id: int, location: 'Location', scale: 'Scale', rotation: float, json_path: str):
        super().__init__(id, location, scale, rotation)
        self.json_path = json_path

    def to_dict(self) -> dict:
        """Serialize the MapAzgaarElement to a dictionary."""
        base_dict = super().to_dict()
        base_dict.update({
            "json_path": self.json_path
        })
        return base_dict

    @staticmethod
    def from_dict(data: dict) -> 'MapAzgaarElement':
        """Reconstruct a MapAzgaarElement from a dictionary."""
        return MapAzgaarElement(
            id=data["id"],
            location=Location.from_dict(data["location"]) if hasattr(Location, "from_dict") else Location(0, 0, 0),
            scale=Scale.from_dict(data["scale"]) if hasattr(Scale, "from_dict") else Scale(1,1,0),
            rotation=data["rotation"],
            json_path=data["json_path"]
        )
