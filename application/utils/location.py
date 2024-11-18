import math

class Location:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"Location(x={self.x}, y={self.y}, z={self.z})"

    def distance_to(self, location: "Location") -> float:
        if not isinstance(location, Location):
            raise TypeError("Argument must be of type Location.")

        dx = self.x - location.x
        dy = self.y - location.y
        dz = self.z - location.z

        return math.sqrt(dx**2 + dy**2 + dz**2)

class Scale:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"Scale(x={self.x}, y={self.y}, z={self.z})"