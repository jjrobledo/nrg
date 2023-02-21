import pandas as pd
import os
import re

# TODO
#  remove call to df cleaner outside of function

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.colheader_justify', 'center')
pd.set_option('display.precision', 3)

path = os.getcwd() + '/shape/csv'


def get_data_files():
    files = os.listdir(path)

    matching_prefix_files = []

    # loop through files in the directory
    for file in files:
        # get the numeric prefix of the file name
        prefix_match = re.match(r'^(\d+)_', file)
        if prefix_match:
            prefix = prefix_match.group(1)
            extension = os.path.splitext(file)[1]
            # add file to matching prefix files list
            found = False
            for prefix_files in matching_prefix_files:
                if prefix_files['prefix'] == prefix:
                    prefix_files['files'][extension] = file
                    found = True
                    break
            if not found:
                matching_prefix_files.append({'prefix': prefix, 'files': {extension: file}})

    return matching_prefix_files


def csv_cleaner(df):
    df = df.drop(
        ['sPerfOrgIn', 'sLeadAgenc', 'sLeadAge_1', 'sSponsor', 'iAllResour', 'bGISAccept', 'iStatusCur', 'sDescrip',
         'geometry'])

    return df


def xlsx_cleaner(df):
    df = df.rename(columns={'NMCRIS Activity #': 'nmcris_number'})
    df = df.drop(['Performing Organization', 'Total Acres', 'Report Title', 'Record Status', 'Performing Org. Report #',
                  'Lead Agency', 'Lead Agency Report #', 'Activity ID', 'Resource Count', 'Starting Date',
                  'Activity Type', 'Author'], axis=1)

    return df


def merged_df_cleaner(df):
    df.loc[df.title.str.isupper(), 'title'] = df.title.str.title()
    df.author = df.author.str.title()
    df.performing_organization = df.performing_organization.str.title()

    return df


def nmcris_file_processor():
    # get a list of all filenames and get the unique parcel ids
    file_dictionary = get_data_files()

    df = pd.DataFrame()

    for dictionary in file_dictionary:
        parcel_id = dictionary['prefix']
        csv_file = dictionary['files']['.csv']
        xlsx_file = dictionary['files']['.xlsx']

        # try opening a csv and xlsx for each parcel_id and assign each to a variable
        csv = pd.read_csv(path + '/' + csv_file)
        xlsx = pd.read_excel(path + '/' + xlsx_file)

        # clean the xlsx
        xlsx = xlsx_cleaner(xlsx)

        # join the csv to the xlsx
        merged = pd.merge(csv, xlsx, on=['nmcris_number'])
        # add parcel_name to merged df
        merged['parcel_id'] = parcel_id

        merged = merged_df_cleaner(merged)
        # merge the cleaned and joined df to the new df
        df = pd.concat([df, merged])

    return df


def save_parcel_stats(df):
    return df.groupby('parcel_id')['acres'].sum()


merged_df = nmcris_file_processor()
print(nmcris_file_processor())
print(save_parcel_stats(merged_df))
