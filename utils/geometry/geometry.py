from abc import ABC
from . import DistanceCalculator
import shapely

class Geometry(ABC):

    def __str__(self):
        pass

    def __repr__(self):
        pass

    def get_distance_to_feature(self):
        pass

class Point(Geometry, shapely.geometry.Point):
    
    def __init__(self, point):
        if type(point) != shapely.geometry.Point:
            raise TypeError("geometry must be of type shapely.geometry.Point")
        self.geometry = point
        
    def __str__(self):
        return f"<Point: {str(self.geometry)}>"
        
    def __repr__(self):
        return str(self.geometry)
        
    def get_distance_to_feature(self, feature):
        try:
            return DistanceCalculator.get_distance_between(self.geometry, feature.point)
        except AttributeError:
            return float("inf")

class Line(Geometry, shapely.geometry.LineString):
    
    def __init__(self, line):
        if type(line) != shapely.geometry.LineString:
            raise TypeError("geometry must be of type shapely.geometry.LineString")
        self.geometry = line
        
    def __str__(self):
        return f"<Line: {str(self.geometry)}>"
        
    def __repr__(self):
        return str(self.geometry)
        
    def get_distance_to_feature(self, feature):
        try:
            point = shapely.ops.nearest_points(self.geometry, feature.point)[0]
            return DistanceCalculator.get_distance_between(point, feature.point)
        except AttributeError:
            return float("inf")
    
class Shape(Geometry, shapely.geometry.Polygon):
    
    def __init__(self, shape):
        if type(shape) != shapely.geometry.Polygon:
            raise TypeError("geometry must be of type shapely.geometry.Polygon")
        self.geometry = shape
        
    def __str__(self):
        return f"<Shape: {str(self.geometry)}>"
        
    def __repr__(self):
        return str(self.geometry)
        
    def get_distance_to_feature(self, feature):
        try:
            if feature.point.within(self.geometry):
                return 0
            else:
                point = shapely.ops.nearest_points(self.geometry, feature.point)[0]
                return DistanceCalculator.get_distance_between(point, feature.point)
        except AttributeError:
            return float("inf")