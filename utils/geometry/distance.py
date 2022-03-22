from math import sin, cos, atan2, radians, sqrt
import shapely.geometry

class DistanceCalculator:
    """
    Outputs the geographic distance between two points on Earth,
        considering its curvature
    Methods:
        get_distance_between: outputs the distance (km) between two
            shapely.geometry.Point objects
        get_distance_between_xy: outputs the distance (km) between two
            points, represented as two sets of latlongs
    """
    @staticmethod
    def get_distance_between(
            p1: shapely.geometry.Point,
            p2: shapely.geometry.Point) -> float:
        if (type(p1) != shapely.geometry.Point or 
                type(p2) != shapely.geometry.Point):
            raise ValueError("p1 and p2 must both be of type shapely.geometry.Point")
        return DistanceCalculator.get_distance_between_xy(p1.y, p1.x, p2.y, p2.x)

    @staticmethod
    def get_distance_between_xy(
            lat1: float, lon1: float, 
            lat2: float, lon2: float) -> float:
        R = 6371
        lat1 = radians(lat1)
        lon1 = radians(lon1)
        lat2 = radians(lat2)
        lon2 = radians(lon2)
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
        return round(R*2*atan2(sqrt(a), sqrt(1-a)), 3)