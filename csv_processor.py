import pandas as pd
import os
import re

# TODO
#  remove call to df cleaner outside of function
# save the final merged df to a file

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
                  'Lead Agency', 'Lead Agency Report #', 'Activity ID', 'Starting Date',
                  'Activity Type', 'Author'], axis=1)

    return df


def merged_df_cleaner(df):
    df['title'] = df['title'].apply(lambda x: x.title() if (isinstance(x, str) and x.isupper()) else x)
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
        merged = pd.merge(csv, xlsx, on='nmcris_number')
        # add parcel_name to merged df
        merged['parcel_id'] = parcel_id
        merged['report_date'] = pd.to_datetime(merged['report_date'])
        merged['year'] = merged['report_date'].dt.year

        merged = merged_df_cleaner(merged)
        # merge the cleaned and joined df to the new df
        df = pd.concat([df, merged])

    return df


def save_parcel_stats(df):
    return df.groupby('parcel_id')['acres'].sum()


import csv


def csv_to_bibtex(csv_file, bibtex_file):
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        with open(bibtex_file, 'w') as g:
            for row in reader:
                g.write("@techreport{" + row['nmcris_number'] + ",\n")
                g.write("  author = {" + row['author'] + "},\n")
                g.write("  institution = {" + row['performing_organization'] + "},\n")
                g.write("  title = {" + row['title'] + "},\n")
                g.write("  year = {" + row['year'] + "},\n")
                g.write("  number = {" + row['nmcris_number'] + "},\n")
                g.write("}\n\n")


merged_df = nmcris_file_processor()
merged_df.to_csv(path + '/final.csv')
print(save_parcel_stats(merged_df))
# Example usage:
csv_to_bibtex(path + '/final.csv', path + '/bib.bib')

print("------------------- Duplicates -------------------")
print(merged_df[merged_df.duplicated()])
