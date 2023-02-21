import sys
import geopandas as gpd


def shapefile_to_csv(filename):
    df = gpd.read_file(filename)
    output_filename = filename.split('.')[0] + '.csv'
    with open(output_filename, 'w') as f:
        for nmcris_number in df.iActivityN.tolist():

            f.write(str(nmcris_number) + ', ')


for filename in sys.argv[1:]:
    if filename.split('.')[-1] != 'shp':
        pass
    else:
        print(f"Converting {filename} to csv")
        shapefile_to_csv(filename)
