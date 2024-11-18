from PIL import Image
import os
import json

class LegendsImage:
    def __init__(self, image_path: str):
        self.image = Image.open(image_path)
        self.width, self.height = self.image.size
        self.file_type = self._get_file_type(image_path)

    def _get_file_type(self, image_path: str):
        """Get the file type from the image extension."""
        _, ext = os.path.splitext(image_path)
        return ext.lower().strip('.')  # e.g., 'jpeg', 'png'

    def __repr__(self):
        return (f"LegendsImage(width={self.width}, height={self.height}, "
                f"file_type={self.file_type})")

    def to_dict(self) -> dict:
        """Serialize the LegendsImage object to a dictionary."""
        return {
            "image_path": self.image_path,
            "width": self.width,
            "height": self.height,
            "file_type": self.file_type
        }

    @staticmethod
    def from_dict(data: dict) -> 'LegendsImage':
        """Reconstruct a LegendsImage object from a dictionary."""
        # Reinitialize the image using the saved image path
        return LegendsImage(data["image_path"])

    def serialize(self) -> str:
        """Serialize the LegendsImage to a JSON string."""
        return json.dumps(self.to_dict())

    @staticmethod
    def deserialize(data: str) -> 'LegendsImage':
        """Deserialize a JSON string to a LegendsImage object."""
        return LegendsImage.from_dict(json.loads(data))