from django.contrib.gis.geoip2 import GeoIP2
import math

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_coords_by_request(request):
    g = GeoIP2()
    ip = get_client_ip(request)
    try:
        lat, lng = g.lat_lon(ip)
    except:
        lat = None
        lng = None
    return lat, lng

def get_distance_by_coords(from_user, to_user): 
    distance = None
    if from_user.lat and to_user.lng:
        earth_radius = 6371; # Радиус земли в километрах
        # ip1 = '178.34.151.48'
        # ip2 = 'yandex.ru'
        # g = GeoIP2()
        lat1, lng1 = from_user.lat, from_user.lng
        lat2, lng2 = to_user.lat, to_user.lng
        
        # print(f"Point A {lat1} {lng1}")
        # print(f"Point B {lat2} {lng2}")

        lng1, lat1, lng2, lat2 = map(math.radians, [lng1, lat1, lng2, lat2])
        
        # print(f"Point A {lat1} {lng1}")
        # print(f"Point B {lat2} {lng2}")

        d_lat = lat2 - lat1
        d_lng = lng2 - lng1
        d = math.sin(d_lat / 2) * math.sin(d_lat / 2) + math.cos(lat1) * math.cos(lat2) * math.sin(d_lng/2) * math.sin(d_lng/2)
        distance = earth_radius * (2 * math.atan2(math.sqrt(d), math.sqrt(1 - d)))
    return distance