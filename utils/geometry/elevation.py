from ..color.color import Color
from PIL import Image
import numpy as np

"""
This script maps a set of lat longs in 
    Singapore to a particular elevation, in metres.

1. Screenshot an image of Singapore's relief map
2. Process it using PIL and numpy
3. Map specific colors in the image to specific elevations
4. Given a set of lat longs, normalise them to get the
    appropriate cell within the picture
5. Use convolution to get a more accurate reading
"""

class Elevation():
    """
    A node in a doubly-linked list representing an elevation point
    It is used to mainly find the elevations just above
        and just below it, so that we can more accurately
        judge the elevations in between
    Fields:
        c: a Color object, noted in RGB
        e: an elevation marker, noted in metres
        higher: the Elevation object for the
            immediate next elevation
        lower: the Elevation object for the
            immediate previous elevation
    Methods:
        set_higher: sets the higher Elevation object
        set_lower: sets the lower Elevation object
        get_diff: a metric of how close the given Color is
            to the Elevation's Color, which lets us work out
            intermediate values, instead of giving arbitrarily
            fixed elevations
    """
    def __init__(self, c: Color, e: float):
        if type(c) != Color:
            raise TypeError("c should be of type Color")
        self.c = c
        self.e = e
        self.higher = None
        self.lower = None
    
    def set_higher(self, other_E) -> None:
        self.higher = other_E
    
    def set_lower(self, other_E) -> None:
        self.lower = other_E

    def get_diff(self, r: float, g: float, b: float) -> float:
        return self.c.get_diff(r, g, b)

class ElevationMap():
    """
    Generates the ElevationMap to query elevations

    Fields:
        arr: a numpy 2D array for containing the RGB
            values of the image
        elevations: an ordered list of Elevation objects
    Methods:
        _set_elevations: a private method for initialising
            the elevation map
        _get_elevation_from_color: a private method for
            getting an elevation from rgb values
        get_elevation: the main method to be used to get elevation
        _convolute: a private method for getting an average
            of a square around the queried location
            in order to get a more accurate reading of elevation
    """
    MIN_LAT = 1.23776
    MIN_LON = 103.61751
    MAX_LAT = 1.47066
    MAX_LON = 104.04360
    D_LAT = MAX_LAT - MIN_LAT
    D_LON = MAX_LON - MIN_LON
    IMG_H = 1030
    IMG_W = 1885
    PATH_TO_ELEVATION_MAP = "utils/assets/singapore-elevation.png"
        
    def __init__(self):
        self._set_elevations()
        img = Image.open(ElevationMap.PATH_TO_ELEVATION_MAP)
        self.arr = np.array(img.convert('RGB'))
        
    def _set_elevations(self) -> None:
        self.elevations = []
        
        # Values obtained by color inspection of the original image
        c_map = {
            168: Color(255, 255, 255),#
            163: Color(219, 203, 201),#
            156: Color(216, 191, 186),#
            141: Color(217, 153, 151),#
            133: Color(224, 147, 145),#
            126: Color(214, 143, 135),#
            113: Color(218, 162, 132),#
            105: Color(185, 134, 118),#
            91: Color(179, 218, 146),#
            76: Color(202, 220, 139),#
            73: Color(180, 219, 130),#
            69: Color(178, 221, 130),#
            54: Color(167, 231, 139),#
            50: Color(164, 223, 150),#
            46: Color(146, 219, 139),#
            44: Color(149, 220, 142),#
            43: Color(147, 225, 134),#
            42: Color(145, 224, 152),#
            38: Color(148, 225, 171),#
            36: Color(152, 220, 163),#
            32: Color(152, 221, 197),#
            30: Color(146, 219, 197),#
            29: Color(150, 220, 168),#
            25: Color(140, 212, 221),#
            24: Color(150, 220, 195),#
            23: Color(167, 221, 230),#
            18: Color(136, 185, 220),#
            17: Color(148, 191, 223),#
            16: Color(138, 182, 223),#
            15: Color(162, 196, 228),#
            14: Color(153, 196, 241),#
            12: Color(135, 168, 218),#
            10: Color(157, 195, 249),#
            8: Color(137, 168, 216),#
            7: Color(138, 156, 219),#
            3: Color(130, 129, 219),#
            2: Color(143, 136, 222),#
            0: Color(134, 122, 239),#
            0: Color(157, 139, 253)#
        }
        
        # Map each node to its lower neighbour
        curr_e = None
        for key, value in c_map.items():
            e = Elevation(value, key)
            e.set_higher(curr_e)
            curr_e = e
            self.elevations.append(e)
            
        # Map each node to its higher neighbour
        curr_e = None
        for e in self.elevations[::-1]:
            e.set_lower(curr_e)
            curr_e = e
            
    def _get_elevation_from_color(
            self, r: float,
            g: float, b: float) -> float:
        
        # Finds the closest matching Elevation object
        # to the RGB value
        min_diff = float("inf")
        result_e = None
        for e in self.elevations:
            diff = e.get_diff(r, g, b)
            if min_diff > diff:
                min_diff = diff
                result_e = e
        lower = float("inf")
        higher = float("inf")

        # Gets the lower and higher neighbour where possible
        if result_e.lower != None:
            lower = result_e.lower.get_diff(r, g, b)
        if result_e.higher != None:
            higher = result_e.higher.get_diff(r, g, b)
        
        # Outputs an elevation based on how "far" the RGB value
        # is from the two surrounding Elevation points
        if lower < higher:
            e = result_e.e
            e_2 = result_e.lower.e
            return (e*lower + e_2*min_diff)/(lower+min_diff)
        else:
            e = result_e.e
            e_2 = result_e.higher.e
            return (e*higher + e_2*min_diff)/(higher+min_diff)
        
    def get_elevation(self, lat: float, long: float) -> float:
        # Raises ValueError if query is out of bounds of Singapore
        if (lat > ElevationMap.MAX_LAT or 
                lat < ElevationMap.MIN_LAT or 
                long > ElevationMap.MAX_LON or 
                long < ElevationMap.MIN_LON):
            raise ValueError("Coordinates out of bounds")
        
        # Normalises the lat long to represent cells in the RGB array
        row = int((lat-ElevationMap.MIN_LAT)
                  *ElevationMap.IMG_H
                  /ElevationMap.D_LAT)
        col = int((long-ElevationMap.MIN_LON)
                  *ElevationMap.IMG_W
                  /ElevationMap.D_LON)
        
        # Convolutes the values for a more accurate result
        return self._convolute(row, col, 2)
    
    def _convolute(self, row: int, col: int, deg: int) -> float:
        # Maps row values to lie within the bounds
        def reflect_row(r):
            if r < 0:
                return abs(r)
            elif r >= ElevationMap.IMG_H:
                return (ElevationMap.IMG_H
                    - abs(ElevationMap.IMG_H-r))
            return r

        # Maps column values to lie within the bounds
        def reflect_col(c):
            if c < 0:
                return abs(c)
            elif c >= ElevationMap.IMG_W:
                return (ElevationMap.IMG_W
                    - abs(ElevationMap.IMG_W-c))
            return c

        # Finds the average elevation amongst the cells in the
        # square surrounding the queried cell
        total_e = 0
        for r in range(-deg, deg+1):
            for c in range(-deg, deg+1):
                total_e += self._get_elevation_from_color(
                    *self.arr[reflect_row(row+r)][reflect_col(col+c)]
                )
        return round(total_e / (deg*2+1)**2, 1)