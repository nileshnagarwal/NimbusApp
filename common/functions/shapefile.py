from django.core import exceptions
import shapefile
from shapely.geometry import Point # Point class
from shapely.geometry import shape # shape() is a function to convert geo objects through the interface
import os
from webapp.settings import BASE_DIR
from masters.models import District

from collections import OrderedDict

import xlrd, xlwt
from xlwt import Workbook

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

# def get_neighbors():
#     """
#     Add neighbors to district model
#     """
#     # Get path to shapefiles
#     shp_path = os.path.join(BASE_DIR, 'shapefiles', 'gadm36_IND_2.shp')
#     shp = shapefile.Reader(shp_path) #open the shapefile
#     all_shapes = shp.shapes() # get all the polygons
#     all_records = shp.records()

#     for i in range(len(all_records)):        
#         GID_2 = all_records[i][5]
#         print('Working on ', GID_2)
#         dist_instance = District.objects.get(unique_id__exact=GID_2)
#         neighbors_list = list(set([str(x).strip() for x in all_records[i][13].split(',') if x]))
#         print('Neighbor List is: ', neighbors_list)
#         for neighbor in neighbors_list:
#             print('Adding neighbor ', neighbor)
#             try:
#                 neighbor_instance = District.objects.get(unique_id__exact=neighbor)
#                 dist_instance.neighbors.add(neighbor_instance)
#             except exceptions.ObjectDoesNotExist:
#                 print('Did not found: ', neighbor)


# def get_neighbors():
#     # Get path to shapefiles
#     shp_path = os.path.join(BASE_DIR, 'shapefiles', 'gadm36_IND_2.shp')
#     shp = shapefile.Reader(shp_path) #open the shapefile
#     all_shapes = shp.shapes() # get all the polygons
#     all_records = shp.records()
#     # copy_path = os.path.join(BASE_DIR, 'shapefiles')
#     # dbf_copy = shapefile.Writer(copy_path+'\dbf_copy')
#     # dbf_copy.fields = list(shp.fields)
#     # dbf_copy.records.extend(shp.records())
#     fields = shp.fields[1:]
#     field_names = [field[0] for field in fields]
#     wb = Workbook()
#     # add_sheet is used to create sheet. 
#     sheet1 = wb.add_sheet('Sheet 1', cell_overwrite_ok=True) 

#     for i in range(len(all_records)):
#         # if i == 290:
#         GID_2 = all_records[i][5]
#         print('Working on: ', GID_2)
#         neighbors_list = [str(x) for x in all_records[i][13].split(',') if x]
#         print('Original Neighbors List: ', neighbors_list)
#         neighbors_list = list(set([str(x).strip() for x in all_records[i][13].split(',') if x]))
#         print('Revised Neighbors List: ', neighbors_list)
#         # neighbors_list = list(OrderedDict.fromkeys(all_records[i][13]))        
#         for neighbor in neighbors_list:
#             print('Searching for ', neighbor, ' in records')
#             # if i == 5:
#             #     print('type(neighbor): ', type(neighbor))
#             #     print('type(neighbors_list): ', type(neighbors_list))
#             #     print('neighbors_list: ', neighbors_list)
#             #     print('type(all_records[5]): ', type(all_records[5]))
#             # name of fields
#             counter = 0
#             for r in shp.shapeRecords():
#                 atr = dict(zip(field_names, r.record))
#                 # print('Checking agnst ', atr['GID_2'])
#                 if atr['GID_2'] == neighbor:
#                     print(neighbor, ' found at position ', counter)
#                     print('Original Neighbors of ',neighbor, ' are: ', all_records[counter][13])
#                     all_records[counter][13] = all_records[counter][13] + ', ' + GID_2
#                     print('Neighbors Revised for ', neighbor, ' to ', all_records[counter][13])
#                     # sheet1.write(counter, 1, atr['NEIGHBORS'])
#                     # sheet1.write(counter, 0, atr['GID_2'])
#                     # atr.__setitem__('NEIGHBORS', '')
#                     # print('Searching for ', all_records[i][5], '. Neighbors Revised for '\
#                     #     , neighbor, ' to ', atr['NEIGHBORS'])
#                 # else:
#                 #     print(atr['GID_2'], ' does not match ', neighbor)
#                 counter+= 1
#     counter = 0
#     for r in all_records:        
#         counter+= 1
#         atr = dict(zip(field_names, r))
#         sheet1.write(counter, 1, atr['NEIGHBORS'])
#         sheet1.write(counter, 0, atr['GID_2'])
#     wb.save('xlwt example.xls')
