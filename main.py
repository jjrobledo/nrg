import os

path = os.getcwd() + '/shape'
print(path)

files = os.listdir(path)

shapefiles = []

for file in files:
    if file.casefold().endswith('.shp'):
        shapefiles.append(file)


print(shapefiles)