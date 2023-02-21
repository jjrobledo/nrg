import os
from shape_to_nmcris_number_csv import process_shapefiles

path = os.getcwd() + '/shape'
print(path)

files = os.listdir(path)

shapefiles = []

for file in files:
    if file.casefold().endswith('.shp'):
        shapefiles.append(file)


process_shapefiles(shapefiles, path)
