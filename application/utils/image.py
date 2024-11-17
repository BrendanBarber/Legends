from PIL import Image
import os

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