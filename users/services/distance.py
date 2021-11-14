import math
from django.contrib.gis.geoip2 import GeoIP2
from geoip2.errors import AddressNotFoundError


def get_client_ip(request):
    """Get client ip from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_coords(request):
    """Get coordinates from request using geoip2 database"""
    g = GeoIP2()
    ip = get_client_ip(request)
    try:
        lat, lng = g.lat_lon(ip)
    except AddressNotFoundError:
        lat = None
        lng = None
    return lat, lng


def get_distance(lat1, lng1, lat2, lng2):
    """Haversine formula for finding the distance by coordinates"""
    earth_radius = 6371  # Радиус земли в километрах
    lng1, lat1, lng2, lat2 = map(math.radians, [lng1, lat1, lng2, lat2])
    d_lat = lat2 - lat1
    d_lng = lng2 - lng1
    d = math.sin(d_lat / 2) * math.sin(d_lat / 2) + math.cos(lat1) * math.cos(lat2) * math.sin(
        d_lng / 2) * math.sin(d_lng / 2)
    distance = earth_radius * (2 * math.atan2(math.sqrt(d), math.sqrt(1 - d)))
    return distance
