#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COnverting DBF files into CSV files

@author: fawdywahyu
"""

# Analisis sebelum tahun 2015 (pakai dbf file, buka dta)
# Convert DBF Files to CSV Files
import csv
from dbfread import DBF

tahun_convert = ['2007', '2008', '2009', '2010',
                 '2011', '2012', '2013', '2014']

for tahun_c in tahun_convert:
    # Specify the path to the .dbf file
    dbf_file_path = f'Data Industri Besar Sedang BPS/ibs_{tahun_c}.dbf'

    # Specify the path to the output CSV file
    csv_file_path = f'Data Industri Besar Sedang BPS/ibs_{tahun_c}.csv'

    # Open the .dbf file
    table = DBF(dbf_file_path)

    # Get the field names from the table
    field_names = table.field_names

    # Open the CSV file in write mode
    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        
        # Write the field names as the header row in the CSV file
        writer.writerow(field_names)
        
        # Iterate over the records in the table
        for record in table:
            # Get the field values as a list
            field_values = [record[field_name] for field_name in field_names]
            
            # Write the field values to the CSV file
            writer.writerow(field_values)

    print(f"Conversion complete. The CSV file is saved at: {csv_file_path}")
