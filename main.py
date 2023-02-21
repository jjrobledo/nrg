import os

path = os.getcwd() + '/shape'
print(path)

files = os.listdir(path)

for file in files:
    if file.casefold().endswith('.shp'):
        print(file)


