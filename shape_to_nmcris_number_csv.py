import os
import geopandas as gpd


def make_directory(path, directory_name):
    directory_name = 'csv'
    output_directory = os.path.join(path, directory_name)

    try:
        # try: make a new directory called csv in the current directory /shape
        os.mkdir(output_directory)
        print("Output folder created")
    except Exception:
        pass

    return output_directory


def create_filename(filename, extension):
    return filename.split('.')[0] + extension


def extract_column(output_directory, output_filename, df, column):
    print('Extracting nmcris numbers')
    with open(os.path.join(output_directory + '/' + output_filename), 'w') as f:
        for nmcris_number in df[column].tolist():
            f.write(str(nmcris_number) + ', ')


def shapefile_to_csv(filename, path):
    # change dir to /shapefile
    # set output_directory to /csv
    os.chdir(path)
    directory_name = 'csv'
    output_directory = make_directory(path, directory_name)

    # read a shapefile in /shape and set an output filename with a csv extension
    df = gpd.read_file(filename)
    df = clean_dataframe(df)

    output_filename = create_filename(filename.split('_')[0] + '_nmcris_numbers', '.csv')

    # open a new file at - ./csv/output_filename.csv and write all rows of the dataframe to the new file
    extract_column(output_directory, output_filename, df, 'nmcris_number')

    df.to_csv(create_filename(output_directory + '/' + filename.split('_')[0] + '_data', '.csv'), index=False)

    os.chdir(path)


def process_shapefiles(filename_list, path):
    for filename in filename_list:
        print(filename)
        if filename.split('.')[-1] != 'shp':
            pass
        else:
            print(f"Converting {filename} to csv")
            shapefile_to_csv(filename, path)


def clean_dataframe(df):
    df = df.drop(
        ['sPerfOrgIn', 'sLeadAgenc', 'sLeadAge_1', 'sSponsor', 'iAllResour', 'bGISAccept', 'iStatusCur', 'sDescrip',
         'geometry'], axis=1)
    df = df.rename(
        columns={'iActivityN': 'nmcris_number', 'dFieldStar': 'field_date', 'sPerfOrgNa': 'performing_organization',
                 'sPerfOrigin': 'performing_organiation_id', 'sReportTit': 'title', 'sAuthor': 'author',
                 'dReportDat': 'report_date', 'bSurvey3': 'survey', 'rSurveyAcr': 'acres'})

    return df
