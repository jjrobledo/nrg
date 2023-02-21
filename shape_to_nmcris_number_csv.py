import os
import geopandas as gpd


def shapefile_to_csv(filename, path):
    os.chdir(path)
    directory = 'csv'
    output_directory = os.path.join(path, directory)

    df = gpd.read_file(filename)
    output_filename = filename.split('.')[0] + '.csv'

    try:
        os.mkdir(output_directory)
        print("Output folder created")
    except Exception:
        pass

    print(output_directory, output_filename)
    with open(os.path.join(output_directory + '/' + output_filename), 'w') as f:
        for nmcris_number in df.iActivityN.tolist():
            f.write(str(nmcris_number) + ', ')

    os.chdir(path)


def process_shapefiles(filename_list, path):
    for filename in filename_list:
        print(filename)
        if filename.split('.')[-1] != 'shp':
            pass
        else:
            print(f"Converting {filename} to csv")
            shapefile_to_csv(filename, path)


def clean_csv(df):
    df = df.drop(['sPerfOrgIn', 'sLeadAgenc', 'sLeadAge_1', 'sSponsor', 'iAllResour', 'bGISAccept', 'iStatusCur', 'sDescrip' ], axis=1)
    df = df.rename(columns={'iActivityN': 'nmcris_number', 'dFieldStar': 'field_date', 'sPerfOrgNa': 'performing_organization', 'sPerfOrigin': 'performing_organiation_id', 'sReportTit': 'title', 'sAuthor': 'author', 'dReportDat': 'report_data', 'bSurvey3': 'survey', 'rSurveyAcr': 'acres'})

    return df
