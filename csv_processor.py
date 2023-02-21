# drop tables from spreadsheets
# df = df.drop(['sPerfOrgIn', 'sLeadAgenc', 'sLeadAge_1', 'sSponsor', 'iAllResour', 'bGISAccept', 'iStatusCur', 'sDescrip','geometry'],axis=1)
# x = x.rename(columns={'NMCRIS Activity #': 'nmcris_number', 'Author': 'author'})
# x = x.drop(['performing_organization', 'total_acres', 'report_title'], axis=1)

# join the csv and xlsx into one df
# parcel_name = filename.split('_')[0]

# add parcel_name to merged df
# merged = pd.merge(csv, x, on=['nmcris_number']

# parcel_name = filename.split('_')[0]

# add parcel_name to merged df
# merged['parcel_id'] = parcel_name


# concat two dataframes
# df = pd.concat([df, merged])


#############################################################

# Create an empty dataframe
import pandas as pd
import os
import re


def get_data_files():
    path = os.getcwd() + '/shape/csv'
    files = os.listdir(path)

    matching_prefix_files = {}

    # loop through files in the directory
    for file in files:
        # get the numeric prefix of the file name
        prefix_match = re.match(r'^(\d+)_', file)
        if prefix_match:
            prefix = prefix_match.group(1)
            # add file to matching prefix files dictionary
            if prefix in matching_prefix_files:
                matching_prefix_files[prefix].append(file)
            else:
                matching_prefix_files[prefix] = [file]

    return matching_prefix_files
