from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .geometry.distance import DistanceCalculator
from .geometry.elevation import ElevationMap
from .utils.utils import check_all_float
from .models import ElevationQuery, DistanceQuery

# Create your views here.
e_map = ElevationMap()

def distance(request):
    def distance_render(values):
        values["latest"] = DistanceQuery.objects.order_by("-time")[:10]
        return render(request, "distance.html", values)

    if request.method == "GET":
        data = request.GET

        if data.get("lat1") == None:
            return distance_render({})

        lat1 = data.get("lat1")
        lon1 = data.get("lon1")
        lat2 = data.get("lat2")
        lon2 = data.get("lon2")

        if not check_all_float(lat1, lon1, lat2, lon2):
            return JsonResponse({"valid": False, "dist": float("inf")})

        dist = DistanceCalculator.get_distance_between_xy(
            float(lat1), float(lon1), float(lat2), float(lon2))
        return JsonResponse({"valid": True, "dist": dist})

    elif request.method == "POST":
        data = request.POST
        lat1 = data.get("lat1")
        lon1 = data.get("lon1")
        lat2 = data.get("lat2")
        lon2 = data.get("lon2")

        values = {
            "lat1": lat1,
            "lon1": lon1,
            "lat2": lat2,
            "lon2": lon2
        }

        if not check_all_float(lat1, lon1, lat2, lon2):
            values["invalid"] = True
            return distance_render(values)

        dist = DistanceCalculator.get_distance_between_xy(
            float(lat1), float(lon1), float(lat2), float(lon2))
        values["dist"] = dist
        query = DistanceQuery(
                lat1=lat1, lon1=lon1,
                lat2=lat2, lon2=lon2,
                dist=dist)
        query.save()
        return distance_render(values)

    return distance_render()

def elevation(request):

    def elevation_render(values):
        values["latest"] = ElevationQuery.objects.order_by("-time")[:10]
        return render(request, "elevation.html", values)

    if request.method == "GET":
        data = request.GET

        if data.get("lat1") == None:
            return elevation_render({})

        lat = data.get("lat")
        lon = data.get("lon")

        if not check_all_float(lat, lon):
            return JsonResponse({"valid": False, "dist": float("inf")})

        elevation = e_map.get_elevation(float(lat), float(lon))
        return JsonResponse({"valid": True, "elevation": elevation})

    elif request.method == "POST":
        dict_to_return = {}
        data = request.POST
        lat = data.get("lat")
        lon = data.get("lon")

        values = {
            "lat": lat,
            "lon": lon,
        }

        if not check_all_float(lat, lon):
            values["invalid"] = True
            return elevation_render(values)

        try:
            elevation = e_map.get_elevation(float(lat), float(lon))
            values["elevation"] = elevation
            query = ElevationQuery(
                lat=lat, lon=lon,
                elevation=elevation)
            query.save()
        except ValueError:
            values["out_of_bounds"] = True
        
        return elevation_render(values)

    return elevation_render({})