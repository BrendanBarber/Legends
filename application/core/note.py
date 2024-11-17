from typing import List, Optional
from application.utils import Location
from application.utils import Timerange
from application.utils import Description
from application.utils import LegendsImage

class Note:
    def __init__(self,
                 location: Location,
                 timerange: Timerange,
                 description: Description,
                 thumbnail: LegendsImage,
                 attached_images: Optional[List[LegendsImage]] = None,
                 parent: Optional['Note'] = None,
                 children: Optional[List['Note']] = None):
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

    def attach_image(self, image: LegendsImage):
        self.attached_images.append(image)

    def __repr__(self):
        return (f"Note(location={repr(self.location)}, timerange={repr(self.timerange)}, "
                f"description={repr(self.description)}, thumbnail={repr(self.thumbnail)}, "
                f"attached_images={len(self.attached_images)} images)")