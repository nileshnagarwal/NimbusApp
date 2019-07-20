from math import radians, cos, sin, asin, sqrt

def haversine(cen_lat, cen_lng, test_lat, test_lng):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    cen_lng, cen_lat, test_lng, test_lat = map(radians, \
        [cen_lng, cen_lat, test_lng, test_lat])

    # haversine formula 
    diff_lng = test_lng - cen_lng 
    diff_lat = test_lat - cen_lat 
    a = sin(diff_lat/2)**2 + cos(cen_lat) * cos(test_lat) * \
        sin(diff_lng/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r