# -*- coding: utf-8 -*-
"""Script to convert the JSON file of all GR and GRP data to a CSV file"""

import pandas
import os

ABSPATH_FILE = os.path.abspath(__file__)
ABSPATH_PROJECT = os.path.dirname(ABSPATH_FILE)


if __name__ == "__main__":

    # Convert JSON to DataFrame
    data_frame = pandas.read_json(os.path.join(ABSPATH_PROJECT, 'data', 'all_gr_data.json'), orient='index')
    data_frame.reset_index(drop=True, inplace=True)


    # Save to CSV
    data_frame.to_csv(os.path.join(ABSPATH_PROJECT, 'data', 'all_gr_data.csv'), index_label= 'id', sep=',', encoding='utf-8')


