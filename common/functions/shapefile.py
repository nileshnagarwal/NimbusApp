import shapefile
from shapely.geometry import Point # Point class
from shapely.geometry import shape # shape() is a function to convert geo objects through the interface
import os
from webapp.settings import BASE_DIR
from masters.models import District

def point_in_polygon(lat, lng):
    """
    Check if point lies within a polygon from polygons defined in a 
    shapefile.
    """

    point = (lng, lat) # an x,y tuple
    # Get path to shapefiles
    shp_path = os.path.join(BASE_DIR, 'shapefiles', 'gadm36_IND_2.shp')
    shp = shapefile.Reader(shp_path) #open the shapefile
    all_shapes = shp.shapes() # get all the polygons
    all_records = shp.records()
    for i in range(len(all_shapes)):
        boundary = all_shapes[i] # get a boundary polygon
        # print('Checking for point ', point, ' in district ', all_records[i][6])
        if Point(point).within(shape(boundary)): # make a point and see if it's in the polygon
            district = all_records[i][6] # get the sixth field of the corresponding record
            state = all_records[i][3]
            print('Point ', point, ' found in district ', district, ', ', state)
            return get_district_id(district, state) # Get district_id from name and return


def get_district_id(district, state):
    """
    Get District Id from District Model using the district name received
    """
    qs = District.objects.filter(district__exact=district, state__exact=state)
    district_ids = qs.values_list('district_id', flat=True)
    id = None
    print (district_ids)
    if len(district_ids) == 1:
        id = district_ids[0]
    return id
